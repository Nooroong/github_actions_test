# from django.contrib import admin
# from django.urls import include, path
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TestViewSet

# viewSet을 등록
router = DefaultRouter()
router.register(r"", TestViewSet, basename="test")

urlpatterns = [
    path("", include(router.urls)),
]