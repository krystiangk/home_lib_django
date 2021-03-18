from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import LANGUAGE_CHOICES
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

class Book(models.Model):

    class Meta:
        ordering = ['id']

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year), MinValueValidator(1400)])
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(default=None, null=True)

    def get_absolute_url(self):
        return reverse('book-create-options')


class Wishlist(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_timestamp = models.DateTimeField(default=timezone.now)


    def get_absolute_url(self):
        return reverse('book-wishlist')