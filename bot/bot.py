from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)

from .base import bot, send_error_message
from .db import is_authorized, unauthorize
from .keyboards import get_menu_keyboard, TEXT_MENU
from .auth import start_auth
from .automessage import handle_auto_message, handle_cancel_message

import logging

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    user = is_authorized(message.from_user.id)

    if not user:
        bot.send_message(message.chat.id, "Boshlashingizdan oldin iltimos quyidagini o'qib chiqing:")
        msg_agreement(message)
        start_auth(message)
        return

    bot.reply_to(message, "Bot siz foydalanishingiz uchun tayyor.", reply_markup=get_menu_keyboard())


@bot.message_handler(func=lambda msg: msg.text == TEXT_MENU['auto_message'])
def handle_auto_message_start(message: Message):    
    try:
        handle_auto_message(message)
    except Exception as e:
        if type(e) == EOFError:
            unauthorize(message.from_user.id)
            start_auth(message)
            return
        
        logging.error(e)
        send_error_message(message)


@bot.message_handler(func=lambda msg: msg.text == TEXT_MENU['cancel_message'])
def handle_auto_message_cancel(message):
    try:
        handle_cancel_message(message)
    except Exception as e:
        logging.error(e)
        send_error_message(message)


agreement_letter = """
Avto xabar bot foydalanuvchilar diqqatiga❗️

Botni ishlatish uchun bir oylik to‘lov qilishingiz kerak bo'ladi. Bot adminiga murojaat qiling @nickphilomath 

Bot telegram profilingizga qo‘shimcha seans bo‘lib kiradi. Yani telegramingizga kod boradi. Shaxsiy xabarlarni bot o‘qimaydi. Sizning nomingizdan xabar yuborishi uchun profilga kiradi.

Botni asosiy profilga ulash tavsiya qilinmaydi. Sababi Telegram spamga qarshi tizimlari doimiy nazorati sababli avto xabar yuborayotgan profillarning bazilarini xabarlarini nomaqbul deb hisoblab bloklab qo‘yish xavfi bor.
"""

def msg_agreement(message: Message):
    bot.send_message(
        message.chat.id,
        agreement_letter
    )


@bot.message_handler(commands=['agreement',])
def send_agreement(message: Message):
    bot.send_message(
        message.chat.id,
        agreement_letter
    )

# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()