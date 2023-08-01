from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket, TicketComment, TicketCommentFile, TicketStatus, TicketLabel
from .forms import TicketCommentForm, TicketCommentFileForm
from tracker.apps.accounts.models import CustomUser
from django.utils import timezone


class TicketListView(generic.ListView):
    model = Ticket
    ordering = ["status", "-pub_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            return queryset.filter(title__icontains=q)
        return queryset


class TicketDetailView(generic.DetailView):
    """
    This view processes all GET requests sent to TicketView.
    """

    model = Ticket
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.get_object().comments.all().order_by("pub_date").select_related()
        context["comments"] = comments
        if self.request.user.is_authenticated:
            context["comment_form"] = TicketCommentForm
            context["file_form"] = TicketCommentFileForm
            context["navigate_to_form"] = self._set_navigation()
            context["attachments"] = self._get_attachment_links()
        return context

    def _set_navigation(self):
        if "attachments" not in self.request.session:
            return False
        elif self.kwargs["pk"] not in self.request.session["attachments"]:
            return False
        else:
            return True

    def _get_attachment_links(self):
        print("the set att function gets executed")
        if "attachments" in self.request.session:
            attachments = self.request.session["attachments"]
            print("atts: ", attachments)
            print(self.kwargs["pk"])
            if self.kwargs["pk"] in attachments:
                return attachments[self.kwargs["pk"]]


class TicketCommentCreateView(LoginRequiredMixin, SingleObjectMixin, generic.FormView):
    """
    This view processes all POST requests sent to TicketView.
    """

    template_name = "core/ticket_detail.html"
    model = Ticket
    form_class = TicketCommentFileForm
    max_attachments = 3

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # for get_success_url kwargs
        if "content" in request.POST:
            # A comment was submitted
            form = TicketCommentForm(self.request.POST)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.ticket = self.object
            comment.pub_date = timezone.now()
            comment.save()
            self.link_attachments(comment)
            return HttpResponseRedirect(self.get_success_url())
        elif "file" in request.FILES:
            # A file was submitted
            return super().post(request, *args, **kwargs)  # calls form_valid

    def form_valid(self, form):
        file = form.save(commit=False)
        file.name = str(self.request.FILES["file"])
        self.add_attachment(file)
        return super().form_valid(form)  # calls get_success_url

    def get_success_url(self):
        return reverse_lazy("core:ticket", kwargs={"pk": self.object.pk})

    def add_attachment(self, file):
        """
        Saves TicketCommentFile instance to db and creates
        attachment session variables associated with it
        """
        ticket_id = self.object.string_id
        if "attachments" not in self.request.session:
            self.request.session["attachments"] = {}
        attachtments = self.request.session["attachments"]
        if ticket_id not in attachtments:
            attachtments[ticket_id] = []
        if len(attachtments[ticket_id]) < self.max_attachments:
            # save to database
            file.save()
            # add to comment (session data)
            attachtments[ticket_id].append({"name": file.name, "id": file.id, "url": file.file.url})
            self.request.session["attachments"] = attachtments

    def link_attachments(self, comment):
        """
        Links attachements in database with the
        comment instance provided.

        - It fills the field "comment_id" in all the TicketCommentFile
         instances that belong to the provided TicketComment instance
        - It removes the attachment session variables for the
        ticket the comment instance belongs to.
        """
        if "attachments" in self.request.session:
            attachments = self.request.session["attachments"]
            ticket_id = self.object.string_id
            if ticket_id in attachments:
                for attachment in attachments[ticket_id]:
                    file = TicketCommentFile.objects.get(id=attachment["id"])
                    file.comment = comment
                    file.save()
                del attachments[ticket_id]
            self.request.session["attachments"] = attachments


class TicketView(generic.View):
    """
    View containing (a) the detail of the ticket,
    (b) the list of comments associated with that
    ticket, and (c) a form to submit a new comment
    """

    def get(self, request, *args, **kwargs):
        view = TicketDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TicketCommentCreateView.as_view()
        return view(request, *args, **kwargs)


class DashboardView(TicketListView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_list_open"] = Ticket.objects.filter(status__name="Open").order_by("-pub_date")
        context["ticket_list_closed"] = Ticket.objects.filter(status__name="Closed").order_by("-pub_date")
        context["ticket_this_week"] = Ticket.get_this_week_stats()
        context["ticket_avg_closing_time"] = Ticket.get_avg_closing_time()
        context["ticket_twelve_days_act"] = Ticket.get_twelve_days_activity()
        context["label_in_open"] = TicketLabel.get_amounts_in_open_tickets()
        context["user_amount"] = CustomUser.objects.count()
        context["user_list_with_assignments"] = CustomUser.get_users_with_assignments()
        return context


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    fields = ["assignees", "title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = TicketStatus.objects.get(name="Open")
        return super().form_valid(form)
