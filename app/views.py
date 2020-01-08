import json
from django.conf import settings
from django.core.mail import send_mail
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives

from .models import Board, Card, BoardList, AuthorizedMember, Comment
from .forms import BoardForm, ListForm, CardForm, UserForm, UserSignupForm, AuthorizedEmail, CommentForm

from .mixin import MembersMixIn


class Boards(TemplateView):
    """
    View the boards of the user
    """

    template_name = 'app/index.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        context = {
            'boards': Board.objects.filter(user=self.request.user, archive=True),
            'archived_boards' : Board.objects.filter(user=self.request.user, archive=False),
            'archived_lists' : BoardList.objects.filter(archive=False),
            'archived_cards' : Card.objects.filter(archive=False),
        }
        return render(self.request, self.template_name, context)


class AddBoard(TemplateView):
    """
    Let the user add new board
    """

    form = BoardForm
    template_name = 'app/create_board.html'
    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name, {'forms': form})

    def post(self, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = self.form(self.request.POST)
        # check whether it's valid:
        if form.is_valid():
            # if it is valid, save(commit=False) gets you a model object, then you can add your extra data
            board = form.save(commit=False)
            # add user data then save() it
            board.user = self.request.user
            board.save()
            # redirect to a home url:
            return redirect('board_view', board.id)
        return render(self.request, self.template_name, {'forms': form})


class BoardView(LoginRequiredMixin,MembersMixIn,TemplateView):
    """
    Redirect the user to the selected board
    """

    authorized_email = AuthorizedEmail
    template_name = 'app/board_view.html'
    template_name_post = 'board_view'
    error = False
    login_url = '/login/'
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        # user board id
        board_id = kwargs.get('id')
        list_object = BoardList.objects.filter(board=board_id)
        list_id = list_object.values_list('id', flat = False)
        # authorized email to access other boards
        authorized_email = self.authorized_email()
        board_list = BoardList.objects.filter(board=board_id, archive=True)
        context = {
            'board' : get_object_or_404(Board, id=board_id),
            'lists' : BoardList.objects.filter(board=board_id, archive=True).order_by('id'),
            'cards' : Card.objects.filter(boardList__in=list_id),
            'boards': Board.objects.filter(user=self.request.user, archive=True),
            'authorized_email' : authorized_email,
            'archived_boards' : Board.objects.filter(user=self.request.user, archive=False),
            'archived_lists' : BoardList.objects.filter(archive=False),
            'archived_cards' : Card.objects.filter(archive=False),
            'members' : AuthorizedMember.objects.filter(board=board_id),
            'members_id' : AuthorizedMember.objects.filter(authorized_email=self.request.user.email),
            'user_member' : AuthorizedMember.objects.filter(authorized_email=self.request.user.email, board=board_id ).exists(),
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board_object = get_object_or_404(Board, id=board_id)
        # create a form instance and populate it with data from the request:
        authorized_email_form = self.authorized_email(self.request.POST)
        # check whether it's valid:
        if authorized_email_form.is_valid():
            authorized_email_form = authorized_email_form.save(commit=False)
            authorized_email_form.user = self.request.user
            authorized_email_form.board = board_object
            authorized_email_form.save()
            invited_user_email = authorized_email_form.authorized_email
            send_mail(
                'Subject here',
                'http://127.0.0.1:8000/board/'+str(board_object.id)+'/confirmation/',
                settings.DEFAULT_FROM_EMAIL,
                [invited_user_email, settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,)
            return redirect(self.template_name_post, board_id)
        return redirect(self.template_name_post, board_id)


class LeaveBoard(TemplateView):
    """
    Let the user leave the board
    """
    
    def get(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        remove_member = AuthorizedMember.objects.filter(id=board_id).delete()
        return redirect('home')


class ConfirmationPage(TemplateView):
    """
    The user will redidect to the confirmation page when clicking the link from their sent email
    """

    template_name = 'app/confirmation.html'
    template_board_url = 'board_view'
    def get(self, *args, **kwargs):
        board_id = kwargs.get('owner_id')
        form = get_object_or_404(AuthorizedMember, board = board_id, authorized_email=self.request.user.email, activation = False)
        return render(self.request, self.template_name, {} )

    def post(self, *args, **kwargs):
        board_id = kwargs.get('owner_id')
        form = get_object_or_404(AuthorizedMember, board = board_id, authorized_email=self.request.user.email, activation = False)
        if form.activation is False:
            form.activation = True
            form.save()
            messages.info(self.request, 'You have successfuly confirm the invitation!')
        return redirect(self.template_board_url, board_id)


class AddList(TemplateView):
    """
    Let the user add new list
    """

    form = ListForm

    template_name = 'app/create_list.html'
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        form = self.form()
        return render(self.request, self.template_name, {'forms': form})

    def post(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board = Board.objects.get(id=board_id)
        # create a form instance and populate it with data from the request:
        form = self.form(self.request.POST)
        # check whether it's valid:
        if form.is_valid():
            form = form.save(commit=False)
            form.board = board
            form.save()
            # redirect to a board views url:
            return redirect('board_view', board_id)
        return render(self.request, self.template_name, {'form': forms})


class AddCard(TemplateView):
    """
    Let the user add new list
    """

    form = CardForm
    template_name = 'app/create_card.html'
    template_name_post = 'board_view'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
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


class EditBoard(TemplateView):
    """
    Let user edit card
    """

    form = CardForm
    template_name = 'app/board_edit.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        board_id = kwargs.get('id')
        board_object = get_object_or_404(Board, id=board_id)
        form = self.form(instance = board_object)
        return render(self.request, self.template_name, {'forms' : form})

    def post(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board_object = get_object_or_404(Board, id=board_id)
        form = self.form(self.request.POST, instance = board_object)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(self.request, self.template_name, {'forms' : form, 'card': card})


class EditCard(TemplateView):
    """
    Let user edit card
    """

    form = CardForm
    template_name = 'app/card_edit.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        form = self.form(instance = card)
        return render(self.request, self.template_name, {'forms' : form, 'card' : card})

    def post(self, *args, **kwargs):
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        form = self.form(self.request.POST, instance = card)
        if form.is_valid():
            form.save()
            return redirect('board_view', card.boardList.board.id)
        else:
            return render(self.request, self.template_name, {'forms' : form, 'card': card})


class DeleteBoard(TemplateView):
    """
    Let the user delete the board
    """

    template_name = 'home'
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        board_id = kwargs.get('id')
        board_object = get_object_or_404(Board, id=board_id)
        board_object.delete()
        return redirect(self.template_name)


class DeleteList(TemplateView):
    """
    Let the user delete the list
    """

    template_name = 'board_view'
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        list_id = kwargs.get('id')
        list_object = get_object_or_404(BoardList, id=list_id)
        list_object.delete()
        return redirect(self.template_name, list_object.board.id)


class DeleteCard(TemplateView):
    """
    Let the user delete the cards
    """

    template_name = 'board_view'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
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
            'cards': Card.objects.filter(boardList__id=list_id, archive=True),
            'archived_boards' : Board.objects.filter(user=self.request.user, archive=False),
            'archived_lists' : BoardList.objects.filter(archive=False),
            'archived_cards' : Card.objects.filter(archive=False),
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
        user = authenticate(self.request, username=username, password=password1, email=email)
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
        return redirect('home')


class EditList(TemplateView):
    """
    Let the user edit list
    """

    form = ListForm
    template_name = 'app/list_edit.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
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


class ShowCards(TemplateView):
    """
    Show Cards
    """
    form = CommentForm
    template_name = 'app/show_cards.html'
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        card_id = kwargs.get('id')
        comment_form = self.form()
        view_comment = Comment.objects.filter(card_id=card_id)
        card_object = Card.objects.get(id=card_id)
        cards = Card.objects.filter(id=card_id)
        return render(self.request, self.template_name, { 'cards' : cards, 'comment_form' : comment_form, 'view_comment' : view_comment, 'card_objects': card_object})


class AddComment(TemplateView):
    """
    Let the users add comments on cards
    """
    
    form = CommentForm
    template_name = 'app/show_cards.html'
    def post(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_object = Card.objects.get(id=card_id)
        comment_data = self.request.POST['comment']
        if comment_data == '':
            return render(self.request, self.template_name, {})
        add_comment = Comment.objects.create(user = self.request.user, comment = comment_data, card = card_object)


class UpdateDescription(TemplateView):
    """
    Let the user update the card descrition
    """

    form = CardForm
    template_name = 'app/update_card_descripion.html'
    def get(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_object = get_object_or_404(Card, id=card_id)
        form = self.form(instance = card_object)
        return render(self.request, self.template_name, {'forms' : form})

    def post(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_object = get_object_or_404(Card, id=card_id)
        form = self.form(self.request.POST, instance = card_object)
        if form.is_valid():
            form.save()
            return redirect('board_view', card_object.boardList.board.id)
        else:
            return render(self.request, self.template_name, {'forms' : form})


class EditComment(TemplateView):
    """
    Able to edit the comment
    """
    form = CommentForm
    template_name = 'app/edit_comment.html'
    def get(self, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment_object = get_object_or_404(Comment, id=comment_id)
        form = self.form(instance = comment_object)
        return render(self.request, self.template_name, {'forms' : form})
    
    def post(self, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment_object = get_object_or_404(Comment, id=comment_id)
        form = self.form(self.request.POST, instance = comment_object)
        if form.is_valid():
            form.save()
            return redirect('board_view', comment_object.card.boardList.board.id)
        else:
            return render(self.request, self.template_name, {'forms' : form})


class DeleteComment(TemplateView):
    """
    Let the user delete the comment
    """

    def get(self, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        board_id = comment.card.boardList.board.id
        comment.delete()
        return redirect('board_view', board_id)



class ArchiveCard(TemplateView):
    """
    Archive Cards
    """

    def get(self, *args, **kwargs):
        card_id = kwargs.get('id')
        card = get_object_or_404(Card, id=card_id)
        if card.archive == False:
            card.archive = True
            card.save()
            return redirect('board_view', card.boardList.board.id)
        elif card.archive == True:
            card.archive = False
            card.save()
            return redirect('board_view', card.boardList.board.id)


class ArchiveList(TemplateView):
    """
    Archive List
    """

    def get(self, *args, **kwargs):
        list_id = kwargs.get('id')
        list_object = get_object_or_404(BoardList, id=list_id)
        if list_object.archive == False:
            list_object.archive = True
            list_object.save()
            return redirect('board_view', list_object.board.id)
        elif list_object.archive == True:
            list_object.archive = False
            list_object.save()
            return redirect('board_view', list_object.board.id)


class ArchiveBoard(TemplateView):
    """
    Archive List
    """

    def get(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board_object = get_object_or_404(Board, id=board_id)
        if board_object.archive == True:
            board_object.archive = False
            board_object.save()
            return redirect('home')
        elif board_object.archive == False:
            board_object.archive = True
            board_object.save()
            return redirect('home')


class UpdateCardAjax(TemplateView):
    """
    Update Cards through ajx
    """

    def get(self, *args, **kwargs):
        to_id = kwargs.get('to_id')
        get_id = kwargs.get('get_id')
        card_object = Card.objects.get(id=get_id)
        card_object.boardList_id = to_id
        card_object.save()


class AuthorizedMembers(TemplateView):
    """
    Let user select members 
    """


    authorized_email = AuthorizedEmail
    template_name = 'app/dev.html'
    def get(self, *args, **kwargs):
        form = self.authorized_email()
        return render(self.request, self.template_name,{ 'authorized_email' : form })

    def post(self, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = self.authorized_email(self.request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return render(self.request, self.template_name,{ 'authorized_email' : form })
            # return redirect('board_view', board.id)
        return render(self.request, self.template_name,{ 'authorized_email' : form })


class AxajCardData(TemplateView):
    
    """
    Send and return data of cards
    """


    form = CardForm
    template_name = 'app/board_view.html'
    template_name_post = 'board_view'

    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name, {'forms' : form})