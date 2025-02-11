from telebot import TeleBot
from telebot.types import (
    WebAppInfo,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from django.conf import settings

# from .text import get_text as _
# from .helpers.auth import register_user
# from .keyboards import get_main_keyboard
# from .handlers import register_handlers

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

WEB_APP_URL = "https://porpoise-knowing-eel.ngrok-free.app"


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    # Create inline keyboard with a Web App button
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        "Open Mini App",
        web_app=WebAppInfo(url=WEB_APP_URL)  # Use WebAppInfo for inline Web Apps
    )
    markup.add(button)
    
    # Send a message with the Web App button
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello! Click the button below to open the mini app:",
        reply_markup=markup
    )


def authorize_step(message: Message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = KeyboardButton(text="share ", request_contact=True)
    markup.add(button)
    msg = bot.reply_to(message, "share your phone b*tch", reply_markup=markup)
    bot.register_next_step_handler(msg, process_phone_step)


def process_phone_step(message: Message):
    # check if user actually share a contact number
    if not message.contact:
        bot.reply_to(message, "you didnt share a contanct, fuck off ")
        return
    
    # check if that contact belongs to user (not other)
    if message.contact.user_id != message.from_user.id:
        bot.reply_to(message, "this contanct is not yours moron")
        return
    
    # register_user(message.contact.phone_number, message.from_user.id)
    bot.reply_to(message, "registery success")


# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()