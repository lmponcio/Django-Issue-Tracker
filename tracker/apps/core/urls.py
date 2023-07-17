from django.urls import path

from .views import DashboardView, TicketListView, TicketDetailView, TicketCreateView

app_name = "core"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("tickets/", TicketListView.as_view(), name="ticket_list"),
    path("tickets/in/<pk>/", TicketDetailView.as_view(), name="ticket_detail"),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket_create"),
]
