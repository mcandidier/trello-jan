from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Board(models.Model):
    """ 
    Creating board model
    """


    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    archive = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    # members = models.ManyToManyField(User)

    def __str__(self):
        return "({}) - {}".format(self.id, self.title)

class BoardList(models.Model):
    """ 
    Creating list model
    """


    orderby =  models.IntegerField(default=True)
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    archive = models.BooleanField(default=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
 
    def __str__(self):
        return "({}) - {} - {}".format(self.orderby, self.id, self.title)

class Card(models.Model):
    """ 
    Creating card model
    """


    title = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    archive = models.BooleanField(default=True)
    boardList = models.ForeignKey(BoardList, on_delete=models.CASCADE)

    def __str__(self):
        return "List id = ({}) - ({}) - {}".format(self.boardList.id, self.id, self.title)


class AuthorizedMember(models.Model):
    """
    Let user add members and autorize them to view the board
    """


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
    authorized_email = models.EmailField(max_length=50)

    def __str__(self):
        return self.authorized_email


# ....
class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title
# ....