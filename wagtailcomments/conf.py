import datetime

from django.conf import settings as django_settings


class DefaultSettings:
    """
    Default settings for wagtailcomments
    """
    WAGTAILCOMMENTS_TIMEOUT = datetime.timedelta(hours=1)


class SettingsHelper:
    def __getattr__(self, key):
        try:
            return getattr(django_settings, key)
        except AttributeError:
            try:
                return getattr(DefaultSettings, key)
            except AttributeError:
                pass
            raise  # Raise the original AttributeError


settings = SettingsHelper()
