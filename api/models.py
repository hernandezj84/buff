from django.db import models
from django.contrib.auth.models import User
import jsonfield


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    workout = jsonfield.JSONField()

    def __str__(self):
        return self.user.email
