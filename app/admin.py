from django.contrib import admin
from .models import Board, BoardList, Card, AuthorizedMember, Comment

admin.site.register(Board)
admin.site.register(BoardList)
admin.site.register(Card)
admin.site.register(AuthorizedMember)
admin.site.register(Comment)

