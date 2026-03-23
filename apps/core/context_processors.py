from functools import lru_cache


def site_settings(request):
    from apps.pages.models import SiteSettings
    try:
        settings_obj = SiteSettings.objects.prefetch_related('social_links').first()
    except Exception:
        settings_obj = None
    return {'site_settings': settings_obj}
