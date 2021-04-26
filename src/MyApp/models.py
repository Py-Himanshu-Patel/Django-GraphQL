from django.db import models

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=100)
	summary = models.TextField()

	def __str__(self) -> str:
		return self.title
