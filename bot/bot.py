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


phone_hashes_holder = dict()


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
    logging.warning(client)    
    
    # client.connect()

    # result = client.send_code_request(phone=phone)
    # logging.warning(result)
    # logging.warning(result.phone_code_hash)

    # client._phone_code_hash = {'998901558090': '967f16199eb7d4647f'}
    # me = client.sign_in(phone=phone, code="34025")
    # logging.warning(me)

    # me = client.get_me()
    # logging.warning(me)

    # client.disconnect()


    return
    result = client.send_code_request(phone=phone)
    # parse the phone (removes + sign)
    phone = utils.parse_phone(phone=phone)
    # save phone hash temporarily
    phone_hashes_holder[phone] = result.phone_code_hash
    
    print(result.phone_code_hash)

    # register_user(message.contact.phone_number, message.from_user.id)
    bot.reply_to(message, "registery success " + message.contact.phone_number + " " + result.phone_code_hash)


# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()