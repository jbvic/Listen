from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("social/", include("social_django.urls", namespace="social")),
    path("create", views.create, name="create"),
    path("entries", views.listout, name="entries"),
    path("logout", views.logout_user, name="logout"),
    path("entries/<int:entry_id>", views.details, name="details"),
]