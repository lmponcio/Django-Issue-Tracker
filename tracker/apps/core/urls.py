from django.urls import path

from .views import dashboard, TicketListView, TicketDetailView

app_name = "core"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("tickets/list/", TicketListView.as_view(), name="ticket-list"),
    path("tickets/<pk>/", TicketDetailView.as_view(), name="ticket-detail"),
]
