from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.db.models import F, Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from tracker.apps.accounts.models import CustomUser


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

    def __str__(self):
        return self.name


class Ticket(TimeStampedModel):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_tickets")
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT)
    labels = models.ManyToManyField(CustomUser, blank=True, related_name="labeled_tickets")
    assignees = models.ManyToManyField(CustomUser, blank=True, related_name="assigned_tickets")
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    closed_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, blank=True, null=True, related_name="closed_tickets"
    )
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # Publication date allows plan publishing in the future (create without publishing)
    pub_date = models.DateTimeField(null=True, blank=True, default=None)
    close_date = models.DateTimeField(null=True, blank=True, default=None)

    @staticmethod
    def get_this_week_stats():
        """Gets published and closed issues since last Sunday"""
        some_day_last_week = timezone.now() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        sunday_of_this_week = monday_of_last_week + timedelta(days=6)
        return {
            "opened": Ticket.objects.filter(pub_date__gte=sunday_of_this_week),
            "closed": Ticket.objects.filter(close_date__gte=sunday_of_this_week),
        }

    @staticmethod
    def get_avg_closing_time():
        finished_tickets = Ticket.objects.filter(pub_date__isnull=False).filter(close_date__isnull=False)
        return finished_tickets.aggregate(avg_time=Avg(F("close_date") - F("pub_date")))["avg_time"]

    @staticmethod
    def get_twelve_days_activity():
        activity = {}
        final_date = timezone.now()
        start_date = final_date - timedelta(days=12)
        activity["opened"] = Ticket.objects.filter(pub_date__range=[start_date, final_date]).select_related()
        activity["closed"] = Ticket.objects.filter(close_date__range=[start_date, final_date]).select_related()
        return activity

    def __str__(self):
        return self.title

    # I might set up this logic by pre-filling the Form in the view
    # I just don't want it to publish immediately if I am using the admin
    #
    # def save(self, *args, **kwargs):
    #     # If pub_date not specified, it gets published immediately
    #     if not self.pub_date:
    #         self.pub_date = self.created
    #     super().save(*args, **kwargs)

    # I might use this method, or I could update it in the view
    #
    # def update_progress(self, value):
    #     if 0 <= value <= 100:
    #         self.progress = value
    #         self.save()
    #     else:
    #         raise ValueError("Invalid progress value. Progress must be between 0 and 100.")


class TicketComment(TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    content = models.TextField(max_length=2000)
