from django.urls import path

from .views import DashboardView, TicketListView, TicketDetailView, TicketCreateView

app_name = "core"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("tickets/list/", TicketListView.as_view(), name="ticket-list"),
    path("tickets/in/<pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
]
