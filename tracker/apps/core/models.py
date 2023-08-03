import json
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.db.models import F, Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from tracker.apps.accounts.models import CustomUser
from .utils import file_path


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
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TicketLabel(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)

    @staticmethod
    def get_amounts_in_open_tickets():
        all_open_tickets = Ticket.objects.filter(status__name="Open").select_related()
        all_labels = {}
        for ticket in all_open_tickets:
            for label in ticket.labels.all():
                if label.name in all_labels:
                    all_labels[label.name] += 1
                else:
                    all_labels[label.name] = 1
        print(all_labels)
        return {"tags": list(all_labels.keys()), "amounts": list(all_labels.values())}

    def __str__(self):
        return self.name


class Ticket(TimeStampedModel):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_tickets")
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT)
    labels = models.ManyToManyField(TicketLabel, blank=True, related_name="labeled_tickets")
    assignees = models.ManyToManyField(CustomUser, blank=True, related_name="assigned_tickets")
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    closed_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, blank=True, null=True, related_name="closed_tickets"
    )
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # pub_date allows to plan publishing in the future (create without publishing)
    pub_date = models.DateTimeField(null=True, blank=True, default=None)
    close_date = models.DateTimeField(null=True, blank=True, default=None)

    @classmethod
    def get_this_week_stats(cls):
        """Gets published and closed issues since last Sunday"""
        some_day_last_week = timezone.now() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        sunday_of_this_week = monday_of_last_week + timedelta(days=6)
        return {
            "opened": cls.objects.filter(pub_date__gte=sunday_of_this_week),
            "closed": cls.objects.filter(close_date__gte=sunday_of_this_week),
        }

    @classmethod
    def get_avg_closing_time(cls):
        finished_tickets = cls.objects.filter(pub_date__isnull=False).filter(close_date__isnull=False)
        avg_time = finished_tickets.aggregate(avg_time=Avg(F("close_date") - F("pub_date")))["avg_time"]
        return avg_time

    @classmethod
    def get_twelve_days_activity(cls):
        """Method that provides data for Team Activity Chart

        It returns a dictionary. It contains:
        - "days" : list of date strings formatted as dd/mm of the last 12 days
        (last date string is `TODAY`)
        - "opened" : list of amounts of issues opened in the each of the 12 days
        - "closed" : list of amounts of issues closed in the each of the 12 days
        - "comments" : list of amounts of comments in issues in each of the 12 days
        - "total" : total amount of coments+closed+opened
        """

        deltas = list(range(12))
        deltas.reverse()
        final_date = timezone.now()
        dates = [final_date - timedelta(days=delta) for delta in deltas]
        days_formatted = [day.strftime("%d/%m") for day in dates]
        days_formatted[-1] = "TODAY"

        opened = [cls.objects.filter(pub_date__day=day.day).count() for day in dates]
        closed = [cls.objects.filter(close_date__day=day.day).count() for day in dates]
        comments = [TicketComment.objects.filter(created__day=day.day).count() for day in dates]

        return {
            "days": days_formatted,
            "opened": opened,
            "closed": closed,
            "comments": comments,
            "total": sum(opened) + sum(closed) + sum(comments),
        }

    @property
    def string_id(self):
        return str(self.id)

    @property
    def stage(self):
        """String representing the stage the task is at

        This string provides insights regarding the level of
        advancement of the ticket. Its value depends on the
        `status` and `progress` of the ticket.
        """
        if self.status.name == "Closed":
            # One stage when ticket Closed
            return "Closed"
        else:
            # Three different stages when ticket Open
            if 70 <= self.progress:
                return "Close to Completion"
            elif 0 < self.progress:
                return "In Progress"
            else:
                return "Pending"

    def save(self):
        if self.status.__str__() == "Closed":
            self.progress = 100
        super().save()

    def get_absolute_url(self):
        return reverse("core:ticket-detail", kwargs={"pk": self.id})

    def __str__(self):
        return self.title


class TicketComment(TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    content = models.TextField(max_length=2000)
    pub_date = models.DateTimeField(null=True, blank=True, default=None)


class TicketFile(models.Model):
    file = models.FileField(upload_to=file_path)
    name = models.CharField(max_length=260)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="files")


class TicketCommentFile(TimeStampedModel):
    file = models.FileField(upload_to=file_path)
    name = models.CharField(max_length=260, blank=True)
    comment = models.ForeignKey(TicketComment, on_delete=models.CASCADE, related_name="files", blank=True, null=True)

    @property
    def minutes_since_creation(self):
        return (timezone.now() - self.created).total_seconds() / 60

    def __str__(self):
        return self.name
