from django.db.models import fields
from rest_framework import serializers
from soko.pizza_app import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"
        read_only_fields = ("buyer", "uid", "topping")
