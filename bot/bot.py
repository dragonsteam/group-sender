from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)

from .base import bot, send_error_message
from .db import is_authorized
from .keyboards import get_menu_keyboard, TEXT_MENU
from .auth import start_auth
from .automessage import handle_auto_message

import logging

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    user = is_authorized(message.from_user.id)

    if not user:
        start_auth(message)
        return

    bot.reply_to(message, "authorized.", reply_markup=get_menu_keyboard())


@bot.message_handler(func=lambda msg: msg.text == TEXT_MENU['auto_message'])
def handle_auto_message_start(message):
    try:
        handle_auto_message(message)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, "Kutilmagan hatolik yuz berdi. Iltimos qayta urinib ko'ring.")


# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()