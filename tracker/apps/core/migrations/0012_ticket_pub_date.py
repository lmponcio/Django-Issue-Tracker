# Generated by Django 4.2.2 on 2023-07-08 02:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_ticket_labels"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="pub_date",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
