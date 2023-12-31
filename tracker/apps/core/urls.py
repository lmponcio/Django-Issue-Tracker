from django.urls import path

from .views import DashboardView, TicketListView, TicketView, TicketCreateView, TicketUpdateView

app_name = "core"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("tickets/", TicketListView.as_view(), name="ticket_list"),
    path("tickets/in/<pk>/", TicketView.as_view(), name="ticket"),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket_create"),
    path("tickets/update/<pk>/", TicketUpdateView.as_view(), name="ticket_update"),
]
