# Generated by Django 2.1.2 on 2018-10-17 23:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_event_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='volunteers',
            field=models.ManyToManyField(related_name='volunteers', to=settings.AUTH_USER_MODEL),
        ),
    ]