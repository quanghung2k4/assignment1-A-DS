from django.db import models

# Create your models here.
from django.db import models

class Cart(models.Model):
    customer_id = models.IntegerField()  # Reference to customer service
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()  # Reference to book service
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_item'