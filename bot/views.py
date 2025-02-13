import telebot
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .bot import bot

import logging


@csrf_exempt
def telegram_webhook(request: HttpRequest):
    if request.method == 'POST':
        # for header, value in request.headers.items():
            # log(f'{header}: {value}')

        secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token', None)
        if secret_token and secret_token == settings.TELEGRAM_WEBHOOK_SECRET_TOKEN:
            # logging.warning("telegram UPDATE")
            # logging.warning(request.body.decode('UTF-8'))
            update = telebot.types.Update.de_json(request.body.decode('UTF-8'))
            bot.process_new_updates(updates=[update])
        else:
            return HttpResponseForbidden()
    return HttpResponse()

"""
to set webhook
https://api.telegram.org/bot<YourBotToken>/setWebhook?url=<YourWebhookURL>

curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
     -H "Content-Type: application/json" \
     -d '{
           "url": "https://your-server.com/webhook",
           "secret_token": "your-secret-token"
         }'
"""