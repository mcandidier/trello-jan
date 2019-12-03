from django.urls import path
from app.views import Boards, AddBoard
from . import views

urlpatterns = [
    path('', Boards.as_view()),
    path('board/new/', AddBoard.as_view(), name='board_new'),
]