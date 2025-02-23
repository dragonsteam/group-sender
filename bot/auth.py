import json
import asyncio
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from telethon import utils, errors
from django.conf import settings

from .base import bot, get_client, send_error_message
from .db import register_or_authorize, get_api_connected, attempt_user_create

import logging


user_auth_data = dict()


def start_auth(message: Message):
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton("📞 Telefon raqamini ulashish", request_contact=True)
        markup.add(button)
        msg = bot.send_message(message.chat.id, "Siz o'z hisobingizga kirmagansiz.\nHisobga kirish uchun telefon raqamingizni ulashing:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        logging.error(e)
        return


def process_phone_step(message: Message):
    # check if user actually share a contact number
    if not message.contact:
        bot.reply_to(message, "Siz kontaktingizni yubormadingiz.")
        return
    
    # check if that contact belongs to user (not other)
    if message.contact.user_id != message.from_user.id:
        bot.reply_to(message, "Bu raqam sizga tegishli emas.")
        return
    phone = message.contact.phone_number

    # check if and api connected to the user
    api = get_api_connected(message.from_user.id)
    if not api:
        attempt_user_create(message.from_user.id, phone)
        bot.send_message(message.chat.id, "Sizda hisob aktivlashtirilmagan.\n Iltimos Adminga habar bering 👉 @nickphilomath")
        return

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    client = get_client(phone, api.api_id, api.api_hash)
    client.connect()

    try:
        result = client.send_code_request(phone=phone)
    except Exception as e:
        logging.error(e)
        send_error_message(message)
        return

    # save phone hash temporarily
    user_auth_data[message.from_user.id] = {
        "phone": phone,
        "phone_hash": result.phone_code_hash
    }
    
    client.disconnect()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("🔑 Kiritish", web_app=WebAppInfo(url=settings.TELEGRAM_WEBHOOK_URL))
    markup.add(button)

    
    msg = bot.reply_to(
        message,
        "Iltimos raqamingizga yuborilgal kodni kiriting:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_verify_code_step)


def process_verify_code_step(message: Message):
    if not message.web_app_data: return
    data = json.loads(message.web_app_data.data)

    verify_code = data['code']

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    auth = user_auth_data.get(message.from_user.id, None)

    if not auth: return

    phone = auth['phone']
    api = get_api_connected(message.from_user.id)

    client = get_client(phone, api.api_id, api.api_hash)
    client.connect()

    # parse the phone (removes '+' sign)
    parsed_phone = utils.parse_phone(phone=phone)

    tg_user = None
    two_step_detected = False

    client._phone_code_hash = {parsed_phone: auth['phone_hash']}

    try:
        tg_user = client.sign_in(phone=phone, code=verify_code)
        is_new_user = register_or_authorize(tg_user.id, phone)
        if is_new_user: msg_new_sub_added(message)
    except errors.SessionPasswordNeededError:
        two_step_detected = True
    except Exception as e:
        logging.error(e)
        send_error_message(message)
        return

    # hande 2fa detection
    if two_step_detected:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton("🔑 Kiritish", web_app=WebAppInfo(url=settings.TELEGRAM_WEBHOOK_URL))
        markup.add(button)
        
        msg = bot.reply_to(
            message,
            "Iltimos 2-bosqich kodni kiriting:",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_2fa_step)
        return

    client.disconnect()

    bot.send_message(message.chat.id, "✅ Siz muvofaqqiyatli ro'yxatdan o'tdingiz. \nBotdan foydalanish uchun yana /start komandasini bosing.")


def process_2fa_step(message: Message):
    if not message.web_app_data: return
    data = json.loads(message.web_app_data.data)

    pass_2fa = data['code']

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    auth = user_auth_data.get(message.from_user.id, None)

    if not auth: return

    phone = auth['phone']
    api = get_api_connected(message.from_user.id)

    client = get_client(phone, api.api_id, api.api_hash)
    client.connect()

    # parse the phone (removes '+' sign)
    parsed_phone = utils.parse_phone(phone=phone)

    client._phone_code_hash = {parsed_phone: auth['phone_hash']}

    try:
        tg_user = client.sign_in(phone=phone, password=pass_2fa)
        is_new_user = register_or_authorize(tg_user.id, phone)
        if is_new_user: msg_new_sub_added(message)
    except Exception as e:
        logging.error(e)
        send_error_message(message)
        return
    
    client.disconnect()
    
    bot.send_message(message.chat.id, "✅ Siz muvofaqqiyatli ro'yxatdan o'tdingiz. \nBotdan foydalanish uchun yana /start komandasini bosing.")


def msg_new_sub_added(message: Message):
    bot.send_message(message.chat.id, "🎁 Sizga bepul 1 haftalik obuna qo'shildi.")