from django.urls import path

from .views import DashboardView, TicketListView, TicketDetailView

app_name = "core"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("tickets/list/", TicketListView.as_view(), name="ticket-list"),
    path("tickets/<pk>/", TicketDetailView.as_view(), name="ticket-detail"),
]
