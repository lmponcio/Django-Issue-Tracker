from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Ticket


# to be removed (testing)
def dashboard(request):
    return HttpResponse("Welcome to the Dashboard")


class TicketListView(generic.ListView):
    model = Ticket


class TicketDetailView(generic.DetailView):
    model = Ticket
    context_object_name = "ticket"
