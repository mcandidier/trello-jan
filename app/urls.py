from django.urls import path
from app.views import Boards, AddBoard, BoardView, AddList
from . import views

urlpatterns = [
    path('', Boards.as_view()),
    path('board/new/', AddBoard.as_view(), name='board_new'),
    path('board/<int:id>/', BoardView.as_view(), name='board_view'),
    path('list/new/<int:id>', AddList.as_view(), name='list_new'),
]