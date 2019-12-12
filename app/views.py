from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Board, Card, BoardList
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import BoardForm, ListForm, CardForm, UserForm, UserSignupForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib import messages


class Boards(TemplateView):

    """
    View the board/s of the user
    """


    template_name = 'app/index.html'
    def get(self, request):
        # select current user and activation
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
        return render(request, self.template_name, {'forms': form})

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = self.form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # if it is valid, save(commit=False) gets you a model object, then you can add your extra data
            form = form.save(commit=False)
            # add user data then save() it
            form.user = request.user
            form.save()
            # redirect to a home url:
            return HttpResponseRedirect('home')
        return render(request, self.template_name, {'forms': form})

class BoardView(TemplateView):

    """
    Redirect the user to the selected board
    """

    template_name = 'app/board_view.html'
    def get(self, *args, **kwargs):
        board_id = kwargs.get('id')
        # iterate board model, if data doesnt exist it will move you to 404 page
        board = get_object_or_404(Board, id=board_id)
        # iterate list model
        list_object = BoardList.objects.filter(board=board_id)
        return render(self.request, self.template_name, {'board': board, 'list_object' : list_object})


class AddList(TemplateView):

    """
    Let the user add new list
    """


    lists = ListForm
    template_name = 'app/create_list.html'
    def get(self, *args, **kwargs):
        lists = self.lists()
        return render(self.request, self.template_name, {'lists': lists})

    def post(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board = Board.objects.get(id=board_id)
        # create a form instance and populate it with data from the request:
        lists = self.lists(self.request.POST)
        # check whether it's valid:
        if lists.is_valid():
            lists = lists.save(commit=False)
            lists.board = board
            lists.save()
            # redirect to a board views url:
            return redirect('board_view', board_id)
        return render(self.request, self.template_name, {'lists': lists})


class AddCard(TemplateView):

    """
    Let the user add new list
    """


    form = CardForm
    template_name = 'app/create_card.html'
    template_name_post = 'board_view'
    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name, {'forms' : form})

    def post(self, *args, **kwargs):
        list_id = kwargs.get('id')
        boardList = BoardList.objects.get(id=list_id)
        # create a form instance and populate it with data from the request:
        form = self.form(self.request.POST)
        # check whether it's valid:
        if form.is_valid():
            form = form.save(commit=False)
            form.boardList = boardList
            form.save()
            # redirect to a board views:
            return redirect(self.template_name_post, boardList.board_id)
        return render(self.request, self.template_name, {'forms': form})


class EditCard(TemplateView):

    """
    Let user edit card
    """

    
    form = CardForm
    template_name = 'app/card_edit.html'
    def get(self, *args, **kwargs):
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        form = self.form(instance = card)
        return render(self.request, self.template_name, {'forms' : form})

    def post(self, *args, **kwargs):
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        form = self.form(self.request.POST, instance = card)
        if form.is_valid():
            form.save()
            return redirect('board_view', card.boardList.board.id)
        else:
            return render(self.request, self.template_name, {'forms' : form})


class DeleteList(TemplateView):

    """
    Let the user delete list
    """

    template_name = 'board_view'
    def get(self, request, *args, **kwargs):
        list_id = kwargs.get('id')
        _list = get_object_or_404(BoardList, id=list_id)
        _list.delete()
        return redirect(self.template_name, _list.board.id)


class DeleteCard(TemplateView):

    """
    Let the user delete cards
    """


    template_name = 'board_view'
    def get(self, request, *args, **kwargs):
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        card.delete()
        return redirect(self.template_name, card.boardList.board.id)


class CardAjax(TemplateView):

    """ 
    Sample ajax page
    """


    template_name = 'app/card_ajax.html'
    def get(self, *args, **kwargs):
        list_id = kwargs.get('id')
        context = {
            'cards': Card.objects.filter(boardList__id=list_id),
        }
        return render(self.request, self.template_name, context)



class SignupView(TemplateView):

    """
    Create user
    """
    

    form = UserSignupForm
    template_name = 'app/signup.html'
    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name,{ 'form' : form})

    def post(self, *args, **kwargs):
        username = self.request.POST['username']
        email = self.request.POST['email']
        password1 = self.request.POST['password1']
        password2 = self.request.POST['password2']
        user = authenticate(self.request, username=username, password=password1)
        exists = User.objects.filter(username=username)
        if self.request.method == 'POST':
            form = self.form(self.request.POST)
            if form.is_valid():
                user = User.objects.create_user(username = username, email = email, password = password1)
                user.save()
                login(self.request, user)
                return redirect('home')
        return render(self.request, self.template_name, {'form': form})

    
class LoginView(TemplateView):
    """
    Let user to login
    """

    template_name = 'app/login.html'
    form = UserForm
    error = False

    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name,{ 'form' : form })

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            username = self.request.POST['username']
            password = self.request.POST['password']
            user = authenticate(self.request,username=username,password=password)
            if user is not None:
                login(self.request, user)
                return redirect('home')
            self.error = True 
        return render(self.request, self.template_name,{'form':form, 'error':self.error})


class LogoutView(TemplateView):

    """
    Logout the user
    """

    def get(self, *args, **kwargs):
        logout(self.request)


class EditList(TemplateView):

    """
    Let the user edit list
    """


    form = ListForm
    template_name = 'app/list_edit.html'
    def get(self, *args, **kwargs):
        list_id = kwargs.get('id')
        list_object = get_object_or_404(BoardList, id=list_id)
        form = self.form(instance = list_object)
        return render(self.request, self.template_name, {'forms' : form})

    def post(self, *args, **kwargs):
        list_id = kwargs.get('id')
        list_object = get_object_or_404(BoardList, id=list_id)
        form = self.form(self.request.POST, instance = list_object)
        if form.is_valid():
            form.save()
            return redirect('board_view', list_object.board.id)
        else:
            return render(self.request, self.template_name, {'forms' : form})