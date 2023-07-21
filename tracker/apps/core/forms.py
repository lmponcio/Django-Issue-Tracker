from django.forms import ModelForm
from .models import TicketComment, TicketCommentFile


class TicketCommentForm(ModelForm):
    class Meta:
        model = TicketComment
        fields = ["content"]


class TicketCommentFileForm(ModelForm):
    class Meta:
        model = TicketCommentFile
        fields = ["file"]
