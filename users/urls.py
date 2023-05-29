from django.contrib import admin
from django.urls import path, include

from users.views import *

urlpatterns = [
    path("user/", UsersAPIView.as_view(), name="username"),
    path("user/<int:pk>", UsersAPIView.as_view(), name="username"),
]
