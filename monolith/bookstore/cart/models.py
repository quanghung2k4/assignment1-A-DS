from django.db import models

# Create your models here.
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

    @classmethod
    def for_customer(cls, customer_id):
        cart, _ = cls.objects.get_or_create(customer_id=customer_id)
        return cart