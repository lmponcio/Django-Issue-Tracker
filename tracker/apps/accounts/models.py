from django.db import models
from django.contrib.auth.models import AbstractUser
from tracker.apps.core.utils import hash_filename
from django.utils import timezone


def profile_img_path(instance, filename):
    """
    Returns a path (filename included) for the uploaded image to be saved
    """
    timestamp = timezone.now()
    timestamp_string = timestamp.strftime("%Y-%m-%d_%H:%M:%S")
    return "profile_images/" + hash_filename(f"{instance.username}{timestamp_string}")


class CustomUser(AbstractUser):
    profile_image = models.ImageField(blank=True, upload_to=profile_img_path)
    position = models.CharField(max_length=50, null=True, blank=True)

    @property
    def open_tickets(self):
        return self.assigned_tickets.filter(status__name="Open").order_by("-pub_date").select_related()

    @property
    def closed_tickets(self):
        return self.assigned_tickets.filter(status__name="Closed").order_by("-pub_date")

    @classmethod
    def get_users_with_assignments(cls):
        uwa = []
        all = cls.objects.all().select_related()
        for user in all:
            tickets = user.assigned_tickets.filter(status__name="Open").order_by("-pub_date")
            if tickets:
                uwa.append((user, tickets[0]))
        return uwa

    def __str__(self):
        if self.first_name and self.last_name:
            return " ".join([self.first_name, self.last_name])
        else:
            return self.username
