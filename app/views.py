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
        return render(request, self.template_name, {'form': form})

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
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})

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
        board_list = BoardList.objects.filter(board=board_id)
        # select list id
        card_query = Card.objects.all()
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
            # redirect to a board views url:
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
        form = self.form()
        return render(self.request, self.template_name, {'form' : form})

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
        return render(self.request, self.template_name, {'form': form})


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
        return render(self.request, self.template_name, {'form' : form})

    def post(self, *args, **kwargs):
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        form = self.form(self.request.POST, instance = card)
        if form.is_valid():
            form.save()
            # import pdb; pdb.set_trace()
            return redirect('board_view', card.boardList.board.id)


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
        if password1 != password2:
            messages.warning(self.request,'Password is not match')
            return render(self.request, 'app/signup.html', {'form': self.form})
        else:
            if user is not None:
                messages.warning(self.request,'The acount is already exist!')
                return render(self.request, 'app/signup.html', {'form': self.form})

            elif exists:
                messages.warning(self.request,'Username is already exist!')
                return render(self.request, 'app/signup.html', {'form': self.form})
            
            else:
                user = User.objects.create_user(username = username, email = email, password = password1)
                user.save()
                login(self.request, user)
                return redirect('/')

    
class LoginView(TemplateView):
    """
    Let user to login
    """


    template_name = 'app/login.html'
    response = HttpResponse()
    form = UserForm
    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name,{ 'form' : form})

    def post(self, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('/')
        else:
            messages.warning(self.request,'Username or Password not correct')
            return render(self.request, 'app/login.html', {'form': self.form})

class LogoutView(TemplateView):
    """
    Logout the user
    """

    def get(self, *args, **kwargs):
        logout(self.request)