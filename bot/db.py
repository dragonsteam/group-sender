from django.utils import timezone
from datetime import timedelta

from .models import TelegramUser


def is_authorized(user_id):
    try:
        user = TelegramUser.objects.get(telegram_id=user_id)
        if not user.is_logged_in: return None
        return user
    except TelegramUser.DoesNotExist:
        return None
    

def register_or_authorize(user_id, phone):
    try:
        user = TelegramUser.objects.get(telegram_id=user_id)
        user.is_logged_in = True
        user.save(update_fields=['is_logged_in'])
    except TelegramUser.DoesNotExist:
        free_sub_days = 7 # 1 week

        TelegramUser.objects.create(
            telegram_id=user_id,
            phone=phone,
            is_logged_in=True,
            subscription=timezone.now().date() + timedelta(days=free_sub_days)
        )
        # return true if user is new
        return True
    return False


def unauthorize(user_id):
    user = TelegramUser.objects.get(telegram_id=user_id)
    user.is_logged_in=False
    user.save(update_fields=['is_logged_in'])


def get_user_phone(user_id):
    return TelegramUser.objects.get(telegram_id=user_id).phone


def has_subscription(user_id):
    user = TelegramUser.objects.get(telegram_id=user_id)
    return user.subscription > timezone.now().date()