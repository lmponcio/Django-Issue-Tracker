from django.db import models
from tracker.apps.accounts.models import CustomUser


class TicketStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)


class Ticket(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_tickets")
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT)
    assignees = models.ManyToManyField(CustomUser, blank=True, related_name="assigned_tickets")
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    content = models.TextField(max_length=2000)


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    pub_date = models.DateTimeField()
    content = models.TextField(max_length=2000)
