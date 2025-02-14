from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton("🤖 Avto xabar jo'natish"),
        KeyboardButton("❌ Avto xabarni to'xtatish"),
    )
    markup.row(
        KeyboardButton("🗂 Papkalarni sozlash"),
        KeyboardButton("👤 Profilni sozlash"),
    )
    return markup