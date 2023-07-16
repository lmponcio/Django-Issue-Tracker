from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser
from .forms import CustomUserCreationForm
from django.http import HttpResponse


class CreateAccountView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/createAccount.html"


class ProfileView(LoginRequiredMixin, generic.DetailView):
    # for LoginRequiredMixin
    login_url = "login"
    # for Detail view
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "user"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status", "Open")
        context["status"] = status
        context["tickets"] = self.object.assigned_tickets.filter(status__name=status).order_by("-pub_date")
        return context
