from django.urls import path
from . import views

urlpatterns = [
    path("room", views.RoomView.as_view()),
    path("rooms", views.RoomViews.as_view()),
    path("status", views.RoomStatus.as_view()),
]
