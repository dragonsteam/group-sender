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
        TelegramUser.objects.create(
            telegram_id=user_id,
            phone=phone,
            is_logged_in=True,
        )


def unauthorize(user_id):
    user = TelegramUser.objects.get(telegram_id=user_id)
    user.is_logged_in=False
    user.save(update_fields=['is_logged_in'])


def get_user_phone(user_id):
    return TelegramUser.objects.get(telegram_id=user_id).phone