from django.urls import path
from . import views

urlpatterns = [
    path("comment", views.CommentView.as_view()),
    path("comments", views.CommentViews.as_view()),
]
