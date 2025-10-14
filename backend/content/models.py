from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save

CACHE_KEY_BOT_SETTINGS = "bot_settings"


class Attachments(models.Model):
    types = {
        'photo': 'Фото',
        'video': 'Видео',
        'document': 'Документ'
    }

    type = models.CharField('Тип вложения', choices=types)
    file = models.FileField('Файл')
    file_id = models.TextField(null=True)
    mailing = models.ForeignKey('Mailing', on_delete=models.SET_NULL, null=True, related_name='attachments')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


class Mailing(models.Model):
    RULES = {
        'OnlyPay': 'Только оплатившим',
        'NotPay': 'Только не оплатившим',
        'All': 'Всем'
    }
    
    text = models.TextField('Текст')
    datetime = models.DateTimeField('Дата/Время')
    is_ok = models.BooleanField('Статус отправки')
    rules = models.CharField(choices=RULES, default='All')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        


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


class VpnSettings(models.Model):
    trial_time = models.IntegerField(default=5, verbose_name='Количество дней пробного периода')
    trafic_day_limit = models.IntegerField(default=15, verbose_name='Лимит трафика в гигабайтах за день')
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return "Настройки VPN"
    
    class Meta:
        verbose_name = "Настройки VPN"
        verbose_name_plural = "Настройки VPN"
        


def clear_bot_settings_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_BOT_SETTINGS)


post_save.connect(clear_bot_settings_cache, sender=WebAppUrl)
post_save.connect(clear_bot_settings_cache, sender=GroupUrl)
post_save.connect(clear_bot_settings_cache, sender=BotTexts)
