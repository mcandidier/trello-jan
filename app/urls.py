from django.urls import path
from app.views import (
    Boards, 
    AddBoard, 
    BoardView,
    AddList, AddCard, MyAjax, DeleteCard, DeleteList, EditCard,
)

urlpatterns = [
    path('', Boards.as_view()),
    path('board/new/', AddBoard.as_view(), name='board_new'),
    path('board/<int:id>/', BoardView.as_view(), name='board_view'),
    path('board/<int:id>/list/new', AddList.as_view(), name='list_new'),
    path('board/list/<int:id>/card/new', AddCard.as_view(), name='card_new'),
    # edit card
    path('board/list/card/edit/<int:id>', EditCard.as_view(), name='card_edit'),
    #  delete list
    path('list/delete/<int:id>/', DeleteList.as_view(), name='delete_list'),
    # delete card data
    path('board/list/cards/delete/<int:id>/', DeleteCard.as_view(), name='delete_card'),
    #ajax urls
    path('list/<int:id>/cards/', MyAjax.as_view(), name='card_list'),
]