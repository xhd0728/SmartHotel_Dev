from django.urls import path
from . import views

urlpatterns = [
    path("order", views.OrderView.as_view()),
    path("orders", views.OrderViews.as_view()),
    path("status", views.OrderStatus.as_view()),
]
