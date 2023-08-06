from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser
from .forms import CustomUserCreationForm
from django.http import HttpResponse


class CustomUserListView(generic.ListView):
    model = CustomUser


class CreateAccountView(LoginRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/create_account.html"


class UpdateAccountView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = "accounts/update_account.html"
    fields = ["first_name", "last_name"]

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"slug": self.object.username})

    def test_func(self):
        """Users can only update their own profile"""
        return self.request.user.pk == int(self.kwargs["pk"])


class ProfileView(generic.DetailView):
    # for LoginRequiredMixin
    login_url = "login"
    # for Detail view
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "user"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = "Closed" if self.request.GET.get("status") == "Closed" else "Open"
        context["status"] = status
        context["tickets"] = self.object.assigned_tickets.filter(status__name=status).order_by("-pub_date")
        return context
