from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"