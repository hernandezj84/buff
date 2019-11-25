from django.db import models
from django.contrib.auth.models import User
import jsonfield


class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    discount = jsonfield.JSONField()
    expire_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.user.email, self.id)


class Commerce(models.Model):
    """Commerce model"""
    commerce = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=100)
    web = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.commerce.email


class Client(models.Model):
    """Client account"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    account = jsonfield.JSONField()

    def __str__(self):
        return self.user.email


class ClientCategory(models.Model):
    """ Client Category"""
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = jsonfield.JSONField()

    def __str__(self):
        return self.user.email


class MatchDocument(models.Model):
    """Match document"""
    commerce = models.ForeignKey(Commerce, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{}-{}".format(self.commerce.company, self.client.user.email, self.discount.title)
