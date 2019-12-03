from django.db import models
from django.conf import settings
from django.utils import timezone

class Board(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)

class BoardList(models.Model):
    title = models.CharField(max_length=30)
    date_created = models.DateField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

class Card(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=200)
    date_created = models.DateField(default=timezone.now)
    _list = models.ForeignKey(BoardList, on_delete=models.CASCADE)
