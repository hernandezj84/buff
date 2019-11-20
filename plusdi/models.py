from django.db import models
from django.contrib.auth.models import User
import jsonfield


class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    discount = jsonfield.JSONField()

    def __str__(self):
        return self.user.email


class Commerce(models.Model):
    """Commerce model"""
    commerce = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.commerce.email
