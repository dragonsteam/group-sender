from telebot.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telethon import functions
from telethon.types import DialogFilterDefault

from .base import bot, get_client, fix_event_loop, send_error_message
from .db import get_user_phone, has_subscription
from .keyboards import get_menu_keyboard
from .scheduler import create_task, stop_task

import logging


auto_msgs_data = dict()


def handle_auto_message(message: Message):
    fix_event_loop()

    msg = "Habar jo'natish uchun papkangizni tanlang:"
    markup = InlineKeyboardMarkup()

    user_phone = get_user_phone(message.from_user.id)

    with get_client(user_phone) as client:
        dialog_filters = client(functions.messages.GetDialogFiltersRequest())

        filters_count = 0
    
        for dialog_filter in dialog_filters.filters:
            if type(dialog_filter) == DialogFilterDefault:
                # markup.add(InlineKeyboardButton("📦 Barcha chatlar", callback_data="select_folder#1"))
                pass
            else:
                # logging.warning(dialog_filter)
                markup.add(InlineKeyboardButton(f"🗂 {dialog_filter.title}", callback_data=f"select_folder#{dialog_filter.id}"))
                filters_count += 1
        
        if not filters_count:
            bot.send_message(message.chat.id, "Sizda papkalar topilmadi. Iltimos telegramda yangi papka qo'shing.")
            return

    bot.send_message(message.chat.id, msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "select_folder#" in call.data)
def handle_select_folder(call):
    bot.answer_callback_query(call.id)

    folder_id = int(call.data.split("#")[1])

    msg = bot.send_message(call.message.chat.id, "📩 Papkaga jo'natish kerak bo'lgan habarni yuboring.")

    bot.register_next_step_handler(msg, handle_task_message, folder_id=folder_id)


def handle_task_message(message: Message, folder_id):
    # save message
    auto_msgs_data[message.from_user.id] = message.text

    try:
        markup = InlineKeyboardMarkup()
        markup.row(
            # InlineKeyboardButton("1", callback_data=f"create_task#{folder_id}#{message.text}#1"),
            InlineKeyboardButton("3️⃣", callback_data=f"create_task#{folder_id}#{message.id}#3"),
            InlineKeyboardButton("5️⃣", callback_data=f"create_task#{folder_id}#{message.id}#5"),
            InlineKeyboardButton("8️⃣", callback_data=f"create_task#{folder_id}#{message.id}#8"),
            InlineKeyboardButton("🔟", callback_data=f"create_task#{folder_id}#{message.id}#10"),
        )

        bot.send_message(message.chat.id, "⏰ Jo'natish intervalini tanlang (minut)", reply_markup=markup)
    except Exception as e:
        logging.error(e)
        send_error_message(message)


@bot.callback_query_handler(func=lambda call: "create_task#" in call.data)
def handle_create_task(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    try:
        # check subscription first
        has_sub = has_subscription(user_id=call.from_user.id)
        if not has_sub:
            bot.send_message(call.message.chat.id, "❌ Sizning obunangiz tugagan. Iltimos adminga murojaat qiling.")
            return

        _, folder_id, message_id, interval = call.data.split("#")
        folder_id = int(folder_id)
        message_id = int(message_id)
        interval = int(interval)

        text = auto_msgs_data.get(call.from_user.id, None)
        if not text:
            bot.send_message(call.message.chat.id, "Out of Memory error.")
            return

        create_task(call.from_user.id, folder_id, text, interval=interval)

        bot.send_message(
            call.message.chat.id,
            f"""✅ Xabar jo'natish boshlandi.\n\nBekor qilish uchun [❌ Avto xabarni to'xtatish] tugmasini bosing.""",
            reply_markup=get_menu_keyboard()
        )
    except Exception as e:
        logging.error(e)
        send_error_message(call.message)


def handle_cancel_message(message: Message):
    # fix_event_loop()

    stop_task(message.from_user.id)

    bot.send_message(message.chat.id, "✅ Barcha avto xabarlar to'xtatildi.")