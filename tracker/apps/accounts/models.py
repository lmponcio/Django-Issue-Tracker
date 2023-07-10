from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    pass

    @classmethod
    def get_users_with_assignments(cls):
        uwa = {}
        all = cls.objects.all().select_related()
        for user in all:
            tickets = user.assigned_tickets.filter(status__name="Open").order_by("-pub_date")
            if tickets:
                uwa[user.username] = tickets
        return uwa

    def __str__(self):
        return self.username
