from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('members.urls')),  # API endpoints
    path('members/', include('members.urls')),
    path('', include('website.urls')),      # Frontend pagina's
]

# Voor het serveren van media en statische bestanden tijdens ontwikkeling
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)