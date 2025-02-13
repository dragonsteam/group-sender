from django.db import models


class TelegramUser(models.Model):
    telegram_id  = models.BigIntegerField(unique=True)
    phone        = models.CharField(max_length=32)
    is_logged_in = models.BooleanField(default=False)