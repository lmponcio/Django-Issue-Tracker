from django.db import models
from tracker.apps.accounts.models import CustomUser
from django.utils.timezone import now


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TicketStatus(TimeStampedModel):
    status = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)


class Ticket(TimeStampedModel):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_tickets")
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT)
    assignees = models.ManyToManyField(CustomUser, blank=True, related_name="assigned_tickets")
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    closed_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, blank=True, null=True, related_name="closed_tickets"
    )
    closed = models.DateTimeField(null=True, blank=True, default=None)


class TicketComment(TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    content = models.TextField(max_length=2000)
