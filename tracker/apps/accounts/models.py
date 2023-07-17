from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import hashlib


def hash_filename(string):
    """
    Returns a hashed filename based on an input string
    """

    string_bytes = string.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string_bytes)
    hashed_filename = sha256_hash.hexdigest()

    return hashed_filename


def profile_img_path(instance, filename):
    """
    Returns a path (filename included) for the uploaded image to be saved
    """
    timestamp = timezone.now()
    timestamp_string = timestamp.strftime("%Y-%m-%d_%H:%M:%S")
    return hash_filename(f"{instance.username}{timestamp_string}")


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
        return self.username
