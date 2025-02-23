from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class TelegramAPI(models.Model):
    api_id   = models.BigIntegerField()
    api_hash = models.CharField(max_length=32)
    phone    = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.api_id}"


class TelegramUser(models.Model):
    api = models.ForeignKey(
        TelegramAPI,
        on_delete=models.SET_NULL,
        null=True,
        related_name='users_connected'
    )
    telegram_id  = models.BigIntegerField(unique=True)
    phone        = models.CharField(max_length=32)
    is_logged_in = models.BooleanField(default=False)
    subscription = models.DateField()

    def clean(self):
        if self.api.users_connected.count() >= 5:
            raise ValidationError("An Api can have a maximum of 5 users connected.")

    def __str__(self):
        return self.phone