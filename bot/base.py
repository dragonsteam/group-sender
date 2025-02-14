import asyncio
from django.conf import settings
from telebot import TeleBot
from telebot.types import Message
from telethon import utils, errors
from telethon.sync import TelegramClient

import logging

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

URL = "https://porpoise-knowing-eel.ngrok-free.app"

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

def get_client(phone) -> TelegramClient:
    # sessions_dir = str(settings.BASE_DIR/'sessions')
    # session_name = sessions_dir + '/' + utils.parse_phone(phone=phone)
    session_name = "sessions/" + utils.parse_phone(phone=phone)
    return TelegramClient(session_name, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)


def fix_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())


def send_error_message(message: Message):
    bot.reply_to(message, "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.")