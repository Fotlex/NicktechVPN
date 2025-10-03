from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save

CACHE_KEY_BOT_SETTINGS = "bot_settings"


class WebAppUrl(models.Model):
    url = models.URLField(
        verbose_name="URL для Web App",
        help_text="Основная ссылка на Telegram Web App.",
        default="https://example.com",
    )

    def __str__(self):
        return "URL для Web App"

    class Meta:
        verbose_name = "URL для Web App"
        verbose_name_plural = "URL для Web App"


class GroupUrl(models.Model):
    url = models.URLField(
        verbose_name="URL группы/канала",
        help_text="Ссылка на Telegram-канал или группу.",
        default="https://t.me/YourChannel",
    )

    def __str__(self):
        return "URL группы/канала"

    class Meta:
        verbose_name = "URL группы/канала"
        verbose_name_plural = "URL группы/канала"


class BotTexts(models.Model):
    start_message = models.TextField(
        verbose_name="Приветственное сообщение (/start)",
        help_text=(
            "Этот текст пользователь видит при первом запуске бота. Используется HTML."
        ),
        default="Открыть приложение VPN",
    )

    def __str__(self):
        return "Тексты бота"

    class Meta:
        verbose_name = "Тексты бота"
        verbose_name_plural = "Тексты бота"


def clear_bot_settings_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_BOT_SETTINGS)


post_save.connect(clear_bot_settings_cache, sender=WebAppUrl)
post_save.connect(clear_bot_settings_cache, sender=GroupUrl)
post_save.connect(clear_bot_settings_cache, sender=BotTexts)
