from .models import AuthorizedMember, Board
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404


class MembersMixIn:
    """
    Member MixIn
    """
    
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        board_id = kwargs.get('id')
        if AuthorizedMember.objects.filter(authorized_email=self.request.user.email, board=kwargs.get('id'), activation = True) or Board.objects.filter(user=self.request.user, archive=True, id=board_id):
            return super().dispatch(self.request, *args, **kwargs)
        raise PermissionDenied