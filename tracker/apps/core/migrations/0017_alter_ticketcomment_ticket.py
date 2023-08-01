# Generated by Django 4.2.2 on 2023-07-18 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_ticketfile_ticketcommentfile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketcomment",
            name="ticket",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="tickets", to="core.ticket"
            ),
        ),
    ]
