from django.urls import path
from . import views

urlpatterns = [
    path("customer", views.CustomerView.as_view()),
    path("customers", views.CustomerViews.as_view()),
    path("status", views.CustomerStatus.as_view()),
]
