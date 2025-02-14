from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)

from .base import bot
from .db import is_authorized
from .keyboards import get_menu_keyboard
from .auth import start_auth

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



# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()