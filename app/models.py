from django.db import models
from django.conf import settings
from django.utils import timezone

class TrelloBoard(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)

class TrelloList(models.Model):
    title = models.CharField(max_length=30)
    date_created = models.DateField(default=timezone.now)
    trello_board = models.ForeignKey(TrelloBoard, on_delete=models.CASCADE)

class TrelloCard(models.Model):
    title = models.CharField(max_length=30)
    date_created = models.DateField(default=timezone.now)
    trello_list = models.ForeignKey(TrelloList, on_delete=models.CASCADE)
