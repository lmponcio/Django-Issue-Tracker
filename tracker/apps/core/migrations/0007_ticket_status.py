# Generated by Django 4.2.2 on 2023-07-06 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_remove_ticket_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="status",
            field=models.ForeignKey(
                default="delete_this_ticket", on_delete=django.db.models.deletion.PROTECT, to="core.ticketstatus"
            ),
            preserve_default=False,
        ),
    ]
