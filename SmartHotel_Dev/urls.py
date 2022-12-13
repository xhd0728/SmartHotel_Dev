from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/user/', include("user.urls")),
    path('api/room/', include("room.urls")),
    path('api/customer/', include("customer.urls")),
    path('api/order/', include("order.urls")),
    path('api/comment/', include("comment.urls")),
]
