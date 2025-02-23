import asyncio
from django.conf import settings
from telebot import TeleBot
from telebot.types import Message
from telethon import utils, errors
from telethon.sync import TelegramClient

from .keyboards import get_menu_keyboard

import logging

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

def get_client(phone, api_id, api_hash) -> TelegramClient:
    # sessions_dir = str(settings.BASE_DIR/'sessions')
    # session_name = sessions_dir + '/' + utils.parse_phone(phone=phone)
    session_name = f"sessions/{api_id}_{utils.parse_phone(phone=phone)}"
    return TelegramClient(session_name, api_id=api_id, api_hash=api_hash)


def fix_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())


def send_error_message(message: Message):
    bot.reply_to(
        message,
        "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.",
        reply_markup=get_menu_keyboard()
    )