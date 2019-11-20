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
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.owner.email
