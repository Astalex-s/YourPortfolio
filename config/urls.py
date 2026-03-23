from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.pages.urls', namespace='pages')),
    path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    # Phase 2 — uncomment when CRM views are ready:
    # path('crm/', include('apps.crm.urls', namespace='crm')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
