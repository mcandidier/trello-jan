from .forms import BoardForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Board, Card, BoardList

class Boards(TemplateView):

    def get(self, request):
        boards = Board.objects.filter(user=request.user)
        return render(request, 'app/index.html', {'boards' : boards})
    
    

class AddBoard(TemplateView):

    form = BoardForm
    def get(self,request):
        form = self.form()
        return render(request, 'app/create_board.html', {'form': form})

    def post(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = BoardForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                # redirect to a new URL:
                return HttpResponseRedirect('/')
        else:
            form = self.form()
        return render(request, 'app/index.html', {'form': form})