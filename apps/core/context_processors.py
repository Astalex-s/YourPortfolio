import os
from functools import lru_cache

from django.conf import settings


def site_settings(request):
    from apps.pages.models import SiteSettings
    try:
        settings_obj = SiteSettings.objects.prefetch_related('social_links').first()
    except Exception:
        settings_obj = None
    return {'site_settings': settings_obj}


def asset_version(request):
    """Версия статики на основе времени изменения файлов — для сброса кэша.

    Статика отдаётся без хэша в имени (Django 6 игнорирует STATICFILES_STORAGE),
    а Nginx помечает её immutable. Параметр ?v= меняется при изменении файла,
    поэтому браузеры подхватывают новую версию без ручного сброса кэша.
    """
    files = [
        settings.BASE_DIR / 'static' / 'css' / 'main.css',
        settings.BASE_DIR / 'static' / 'js' / 'main.js',
    ]
    try:
        version = int(max(os.path.getmtime(f) for f in files if os.path.exists(f)))
    except (ValueError, OSError):
        version = 1
    return {'asset_version': version}
