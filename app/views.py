from .forms import BoardForm, ListForm, CardForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Board, Card, BoardList

class Boards(TemplateView):
    """
    View the board/s of the user
    """
    template_name = 'app/index.html'
    def get(self, request):
        boards = Board.objects.filter(user=request.user, activation=True)
        return render(request, self.template_name, {'boards' : boards})


class AddBoard(TemplateView):
    """
    Let the user add new board
    """

    form = BoardForm
    template_name = 'app/create_board.html'
    def get(self,request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = self.form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            form = self.form()
        return render(request, self.template_name, {'form': form})

class BoardView(TemplateView):
    """
    Redirect the user to the selected board
    """

    template_name = 'app/board_view.html'
    # query_boardList = BoardList.objects.all()
    def get(self, *args, **kwargs):
        board_id = kwargs.get('id')
        # iterate board model
        board = get_object_or_404(Board, id=board_id)
        # iterate list model
        board_list = BoardList.objects.filter(board=board_id)
        # iterate cards model
        q = board_list.values()[0].get('id')
        card_query = Card.objects.filter(boardList = q)
        # import pdb; pdb.set_trace()
        return render(self.request, self.template_name, {'board': board, 'board_list' : board_list, 'card_views' : card_query})


class AddList(TemplateView):
    """
    Let the user add new list
    """


    list_view = ListForm
    template_name = 'app/create_list.html'
    def get(self, *args, **kwargs):
        list_view = self.list_view()
        return render(self.request, self.template_name, {'list_view': list_view})

    def post(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board = Board.objects.get(id=board_id)
        # create a form instance and populate it with data from the request:
        list_view = self.list_view(self.request.POST)
        # check whether it's valid:
        if list_view.is_valid():
            list_view = list_view.save(commit=False)
            list_view.board = board
            list_view.save()
            # redirect to a new URL:
            return redirect('board_view', board_id)
        return render(self.request, self.template_name, {'list_view': list_view})


class AddCard(TemplateView):
    """
    Let the user add new list
    """


    form = CardForm
    template_name = 'app/create_card.html'
    template_name_post = 'board_view'
    def get(self, *args, **kwargs):
        card_list = self.card_list()
        return render(self.request, self.template_name, {'form' : form})

    def post(self, *args, **kwargs):
        list_id = kwargs.get('id')
        boardList = BoardList.objects.get(id=list_id)
        # create a form instance and populate it with data from the request:
        card_list = self.card_list(self.request.POST)
        # check whether it's valid:
        if card_list.is_valid():
            card_list = card_list.save(commit=False)
            card_list.boardList = boardList
            card_list.save()
            # redirect to a new URL:
            return redirect(self.template_name_post, list_id)
        return render(self.request, self.template_name_post, {'form': card_list})