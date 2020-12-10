from django.db import models
from django.contrib.auth.models import User

class Pizza(models.Model):
    """
    Model for the pizza data
    """
    SIZE = [
        ('SM', 'Small'),
        ('MD', 'Medium'),
        ('LG', 'Large'),
    ]
    size = models.CharField(max_length=10,choices=SIZE,default='SM')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        unique_together = ('seller', 'size', 'price',)

    def __str__(self) -> str:
        """
        return a string representation of the model
        """
        return self.size


class ToppingType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        """
        return a string representation of the model
        """
        return self.name
    

class Category(models.Model):
    topping_type = models.ForeignKey(ToppingType, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        """
        return a string representation of the model
        """
        return str(self.price)

class Topping(models.Model):
    """
    Model for the toppings data
    """
    name = models.CharField(max_length=150)
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        """
        return a string representation of the model
        """
        return self.name

class Order(models.Model):
    uid = models.CharField(max_length=150)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, blank=True, null=True)
    topping = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        return a string representation of the model
        """
        return self.uid
