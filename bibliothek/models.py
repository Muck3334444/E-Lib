from django.db import models

class Book(models.Model):
    bookName = models.CharField(max_length=256)

# Create your models here.
