from django.urls import path
from app.views import (
    Boards, 
    AddBoard, 
    BoardView,
    AddList, AddCard, CardAjax, DeleteCard, DeleteList, EditCard, 
    EditList,
    LoginView,
    SignupView,
    LogoutView,
    ShowCards,


    SampleInput,
    OutputAjax,
    OutputAjaxs,
)

urlpatterns = [
    path('', Boards.as_view(), name='home'),
    # login page
    path('login/', LoginView.as_view(), name='login'),
    # logout
    path('logout/', LogoutView.as_view(), name='logout'),
    # sign up page
    path('signup/', SignupView.as_view(), name='signup'),
    # add board
    path('board/new/', AddBoard.as_view(), name='board_new'),
    # view the user board
    path('board/<int:id>/', BoardView.as_view(), name='board_view'),
    # add user list
    path('board/<int:id>/list/new', AddList.as_view(), name='list_new'),
    # add user card
    path('board/list/<int:id>/card/new', AddCard.as_view(), name='card_new'),
    # edit card
    path('board/list/card/edit/<int:id>', EditCard.as_view(), name='card_edit'),
    #  delete list
    path('board/list/delete/<int:id>/', DeleteList.as_view(), name='delete_list'),
    # delete card data
    path('board/list/cards/delete/<int:id>/', DeleteCard.as_view(), name='delete_card'),
    # Edit list
    path('board/<int:board_id>/list/edit/<int:id>', EditList.as_view(), name='list_edit'),
    # 
    path('board/show/cards/<int:id>', ShowCards.as_view(), name='show_cards'),

    #ajax urls
    path('list/<int:id>/cards/', CardAjax.as_view(), name='card_list'),

    # for dev only
    path('board/dev/', SampleInput.as_view(), name='dev'),
    # ajax output
    path('board/output/ajax/', OutputAjax.as_view(), name='output_ajax'),
    path('board/output/ajax/<int:id>', OutputAjaxs.as_view(), name='output_ajax'),
]