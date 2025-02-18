from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

TEXT_MENU = {
    "auto_message":     "🤖 Avto xabar jo'natish",
    "cancel_message":   "❌ Avto xabarni to'xtatish",
    "folder_settings":  "🗂 Papkalarni sozlash",
    "profile_settings": "👤 Profilni sozlash",
}


def get_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(TEXT_MENU['auto_message']),
        KeyboardButton(TEXT_MENU['cancel_message']),
    )
    # markup.row(
    #     KeyboardButton(TEXT_MENU['folder_settings']),
    #     KeyboardButton(TEXT_MENU['profile_settings']),
    # )
    return markup