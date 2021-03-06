from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Book(models.Model):
    FRENCH = 'FR'
    ENGLISH = 'EN'
    NORWEGIAN = 'NO'
    POLISH = 'PL'
    RUSSIAN = 'RU'
    UKRAINIAN = 'UA'
    LANGUAGE_CHOICES = [
        (FRENCH, 'French'),
        (ENGLISH, 'English'),
        (NORWEGIAN, 'Norwegian'),
        (POLISH, 'Polish'),
        (RUSSIAN, 'Russian'),
        (UKRAINIAN, 'Ukrainian'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(default=None, null=True)

    def get_absolute_url(self):
        return reverse('book-create')



