from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket, TicketComment, TicketStatus, TicketLabel
from .forms import TicketCommentForm
from tracker.apps.accounts.models import CustomUser


class TicketListView(generic.ListView):
    model = Ticket


class TicketDetailView(generic.DetailView):
    model = Ticket
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = TicketComment.objects.filter(ticket=self.get_object()).order_by("created")
        context["comments"] = comments
        if self.request.user.is_authenticated:
            context["comment_form"] = TicketCommentForm(instance=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        new_comment = TicketComment(
            content=request.POST.get("content"), author=self.request.user, ticket=self.get_object()
        )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


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


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    fields = ["assignees", "title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = TicketStatus.objects.get(name="Open")
        return super().form_valid(form)
