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
    ArchiveCard,
    ArchiveList,
    DeleteBoard,
    ArchiveBoard,
    EditBoard,


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
    # delete board
    path('board/delete/<int:id>/', DeleteBoard.as_view(), name='delete_board'),
    # edit board
    path('board/edit/<int:id>', EditBoard.as_view(), name='board_edit'),
    # edit card
    path('board/list/card/edit/<int:id>', EditCard.as_view(), name='card_edit'),
    #  delete list
    path('board/list/delete/<int:id>/', DeleteList.as_view(), name='delete_list'),
    # delete card
    path('board/list/card/delete/<int:id>/', DeleteCard.as_view(), name='delete_card'),
    # archive board
    path('board/archive/<int:id>/', ArchiveBoard.as_view(), name='archive_board'),
    # archive list
    path('board/list/archive/<int:id>/', ArchiveList.as_view(), name='archive_list'),
    # archive card
    path('board/list/card/archive/<int:id>/', ArchiveCard.as_view(), name='archive_card'),
    # Edit list
    path('board/<int:board_id>/list/edit/<int:id>', EditList.as_view(), name='list_edit'),
    # display card modal
    path('board/show/cards/<int:id>', ShowCards.as_view(), name='show_cards'),

    #ajax urls
    path('list/<int:id>/cards/', CardAjax.as_view(), name='card_list'),

    # for dev only
    path('board/dev/', SampleInput.as_view(), name='dev'),
    # ajax output
    path('board/output/ajax/', OutputAjax.as_view(), name='output_ajax'),
    path('board/output/ajax/<int:id>', OutputAjaxs.as_view(), name='output_ajax'),
]