from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0
    

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    def __str__(self):
        return f'Order {self.order_id} by {self.user.username}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.order_id}'

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
