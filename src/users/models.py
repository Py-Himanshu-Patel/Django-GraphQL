from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	email = models.EmailField(blank=False, max_length=100, verbose_name="email")
	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'email'
