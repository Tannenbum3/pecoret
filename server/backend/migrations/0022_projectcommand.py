# Generated by Django 4.2.4 on 2023-09-16 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0021_apitoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=512)),
                ('date_run', models.DateTimeField(default=django.utils.timezone.now)),
                ('output', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.project')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['project', 'date_run'],
            },
        ),
    ]
