from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Board(models.Model):
    """ 
    Creating board model
    """


    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    archive = models.BooleanField(default=True)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return "({}) - {}".format(self.id, self.title)

class BoardList(models.Model):
    """ 
    Creating list model
    """


    title = models.CharField(max_length=30)
    date_created = models.DateField(default=timezone.now)
    archive = models.BooleanField(default=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
 
    def __str__(self):
        return "({}) - {}".format(self.id, self.title)

class Card(models.Model):
    """ 
    Creating card model
    """


    title = models.CharField(max_length=30)
    date_created = models.DateField(default=timezone.now)
    archive = models.BooleanField(default=True)
    boardList = models.ForeignKey(BoardList, on_delete=models.CASCADE)

    def __str__(self):
        return "({}) - {}".format(self.id, self.title)