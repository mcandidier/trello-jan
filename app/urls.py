from django.urls import path
from app.views import Boards, AddBoard, BoardView, AddList, AddCard
from . import views

urlpatterns = [
    path('', Boards.as_view()),
    path('board/new/', AddBoard.as_view(), name='board_new'),
    path('board/<int:id>/', BoardView.as_view(), name='board_view'),
    path('board/<int:id>/list/new', AddList.as_view(), name='list_new'),
    path('board/list/card/new/<int:id>', AddCard.as_view(), name='card_new'),
]