# from django.contrib import admin
# from django.urls import include, path
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, ResumeViewSet, UserViewSet

# viewSet을 등록
router = DefaultRouter()
router.register(r"", TestViewSet, basename="test")
router.register(r"resumes", ResumeViewSet, basename="resumes")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]