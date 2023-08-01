# Generated by Django 4.2.2 on 2023-07-18 12:04

from django.db import migrations, models
import django.db.models.deletion
import tracker.apps.core.utils


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_alter_ticket_labels"),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to=tracker.apps.core.utils.file_path)),
                ("name", models.CharField(max_length=260)),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="files", to="core.ticket"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TicketCommentFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to=tracker.apps.core.utils.file_path)),
                ("name", models.CharField(max_length=260)),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="files", to="core.ticketcomment"
                    ),
                ),
            ],
        ),
    ]
