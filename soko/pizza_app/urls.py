"""urls for orders"""
from django.urls import path

# local imports
from soko.pizza_app import views

app_name = "order"

urlpatterns = [path("order", views.OrderList.as_view(), name="orders")]
