from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

    email = models.EmailField(blank=False, max_length=254)
