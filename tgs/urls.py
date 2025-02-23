from django.contrib import admin
from django.urls import path, include

from bot.views import telegram_webhook

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('webhook', telegram_webhook, name="telegram-webhook"),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    # path('api/', include('api.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += [
#         path('monitoring/', include('monitoring.urls')),
#     ]