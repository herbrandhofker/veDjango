from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('members.urls', namespace='members-api')),  # Changed namespace
    path('', include('website.urls', namespace='website')),
]