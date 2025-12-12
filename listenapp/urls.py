from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("social/", include("social_django.urls", namespace="social")),
    path("create", views.create, name="create"),
    path("entries", views.listout, name="entries"),
    path("logout", views.logout_user, name="logout"),
    path("entries/<int:entry_id>", views.details, name="details"),
    path("rectracks/", views.rectracks, name="rectracks"),
    path("discovery", views.discovery, name="discovery"),
    path("comment_create/<int:entry_id>", views.comment_create, name="comment_create"),
    path("comment_delete/<int:comment_id>", views.comment_delete, name="comment_delete"),
    path("entry_delete/<int:entry_id>", views.entry_delete, name="entry_delete"),
    path("reply_create/<int:comment_id>", views.reply_create, name="reply_create"),
    path("reply_delete/<int:reply_id>", views.reply_delete, name="reply_delete"),
    path("settings", views.settings, name="settings"),
    path("open_reply_thread/<int:comment_id>", views.open_reply_thread, name="open_reply_thread"),
]