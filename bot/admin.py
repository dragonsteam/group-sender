from django.contrib import admin

from .models import TelegramAPI, TelegramUser

admin.site.register(TelegramAPI)
admin.site.register(TelegramUser)