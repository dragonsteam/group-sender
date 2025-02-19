from django.db import models
from django.utils import timezone


class TelegramUser(models.Model):
    telegram_id  = models.BigIntegerField(unique=True)
    phone        = models.CharField(max_length=32)
    is_logged_in = models.BooleanField(default=False)
    subscription = models.DateField(default=timezone.now)