from django.forms import ModelForm
from .models import TicketComment


class TicketCommentForm(ModelForm):
    class Meta:
        model = TicketComment
        fields = ["content"]
