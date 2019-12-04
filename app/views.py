from .forms import BoardForm, ListForm
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
    def get(self, *args, **kwargs):
        id = kwargs.get('id')
        board = get_object_or_404(Board, id=id)
        board_list = BoardList.objects.filter(board=id)
        return render(self.request, self.template_name, {'board': board, 'board_list' : board_list})


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
        id = kwargs.get('id')
        board = Board.objects.get(id=id)
        # create a form instance and populate it with data from the request:
        list_view = self.list_view(self.request.POST)
        # check whether it's valid:
        if list_view.is_valid():
            list_view = list_view.save(commit=False)
            list_view.board = board
            list_view.save()
            # redirect to a new URL:
            return redirect('board_view', id)
        return render(self.request, self.template_name, {'list_view': list_view})