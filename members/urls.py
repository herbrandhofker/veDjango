from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'members', views.MemberViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('test-form/', views.test_form_view, name='test_form'),
]