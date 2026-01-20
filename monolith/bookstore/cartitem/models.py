from django.db import models

# Create your models here.
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart_id = models.IntegerField()
    book_id = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"CartItem {self.id} in Cart {self.cart_id}"