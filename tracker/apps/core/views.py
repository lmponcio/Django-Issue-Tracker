from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Ticket, TicketStatus, TicketLabel
from tracker.apps.accounts.models import CustomUser


class TicketListView(generic.ListView):
    model = Ticket


class TicketDetailView(generic.DetailView):
    model = Ticket
    context_object_name = "ticket"


class DashboardView(TicketListView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_list_open"] = Ticket.objects.filter(status__name="Open").order_by("-pub_date")
        context["ticket_list_closed"] = Ticket.objects.filter(status__name="Closed").order_by("-pub_date")
        context["ticket_this_week"] = Ticket.get_this_week_stats()
        context["ticket_avg_closing_time"] = Ticket.get_avg_closing_time()
        context["ticket_twelve_days_act"] = Ticket.get_twelve_days_activity()
        context["label_amounts"] = TicketLabel.get_amounts_in_open_tickets()
        context["user_amount"] = CustomUser.objects.count()
        context["user_list_with_assignments"] = CustomUser.get_users_with_assignments()
        # TODO:
        ## Add users with open tickets
        return context
