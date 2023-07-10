# Generated by Django 4.2.2 on 2023-07-10 03:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_ticket_progress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="labels",
            field=models.ManyToManyField(blank=True, related_name="labeled_tickets", to="core.ticketlabel"),
        ),
    ]
