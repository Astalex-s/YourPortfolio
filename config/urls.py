from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.pages.urls', namespace='pages')),
    path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    # path('crm/', include('apps.crm.urls', namespace='crm')),
]

# JWT endpoints (доступны только если DRF установлен)
try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    urlpatterns += [
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
except ImportError:
    pass

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
