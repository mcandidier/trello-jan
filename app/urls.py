from django.urls import path
from app.views import (
    Boards, 
    AddBoard, 
    BoardView,
    AddList, AddCard, CardAjax, DeleteCard, DeleteList, EditCard, EditList,
    LoginView,
)

urlpatterns = [
    path('', Boards.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    # add board
    path('board/new/', AddBoard.as_view(), name='board_new'),
    # board view
    path('board/<int:id>/', BoardView.as_view(), name='board_view'),
    #ajax urls
    path('list/<int:id>/cards/', CardAjax.as_view(), name='card_list'),
    # add list
    path('board/<int:id>/list/new', AddList.as_view(), name='list_new'),
    # add card
    path('board/list/<int:id>/card/new', AddCard.as_view(), name='card_new'),
    # edit card
    path('board/list/card/edit/<int:id>', EditCard.as_view(), name='card_edit'),
    #  delete list
    path('board/list/delete/<int:id>/', DeleteList.as_view(), name='delete_list'),
    # edit list
    path('board/<int:pk>/list/edit/<int:id>', EditList.as_view(), name='edit_list'),
    # delete card data
    path('board/list/cards/delete/<int:id>/', DeleteCard.as_view(), name='delete_card'),
]