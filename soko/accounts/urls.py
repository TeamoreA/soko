from django.urls import path

import soko.accounts.views as views

app_name = "authentication"

urlpatterns = [
    path("auth/register", views.RegisterAPIView.as_view(), name="user_signup"),
    path("auth/login", views.LoginAPIView.as_view(), name="user_login"),
]
