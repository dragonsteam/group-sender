from django.contrib import admin
from django.urls import path, include

from bot.views import telegram_webhook


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    path('webhook/', telegram_webhook, name="telegram-webhook"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += [
#         path('monitoring/', include('monitoring.urls')),
#     ]