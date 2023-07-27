# Generated by Django 4.2.1 on 2023-07-11 04:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0008_remove_finding_host_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="advisory",
            name="custom_report_title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="advisory",
            name="hide_advisory_id_in_report",
            field=models.BooleanField(default=False),
        ),
    ]