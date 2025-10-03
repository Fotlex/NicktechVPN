from asgiref.sync import sync_to_async
from django.core.cache import cache

from backend.content.models import CACHE_KEY_BOT_SETTINGS, BotTexts, GroupUrl, WebAppUrl


@sync_to_async
def get_bot_settings():
    cached_settings = cache.get(CACHE_KEY_BOT_SETTINGS)
    if cached_settings:
        return cached_settings

    webapp_url, _ = WebAppUrl.objects.get_or_create(pk=1)
    group_url, _ = GroupUrl.objects.get_or_create(pk=1)
    bot_texts, _ = BotTexts.objects.get_or_create(pk=1)

    settings = {
        "webapp_url": webapp_url.url,
        "group_url": group_url.url,
        "start_message": bot_texts.start_message,
    }

    cache.set(CACHE_KEY_BOT_SETTINGS, settings, timeout=None)
    return settings
