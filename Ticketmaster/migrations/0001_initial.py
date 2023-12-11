# Generated by Django 4.2.7 on 2023-12-08 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventid', models.CharField(max_length=200, verbose_name='Event Name')),
                ('name', models.CharField(max_length=200, verbose_name='Event Name')),
                ('venue', models.CharField(max_length=200, verbose_name='Venue Name')),
                ('address', models.CharField(max_length=150, verbose_name='Venue Address')),
                ('city', models.CharField(max_length=150, verbose_name='Event City')),
                ('state', models.CharField(max_length=100, verbose_name='Event State')),
                ('start_date', models.CharField(max_length=100, verbose_name='Event Date')),
                ('start_time', models.CharField(max_length=100, verbose_name='Event Time')),
                ('ticket_link', models.URLField(verbose_name='Ticket Link')),
                ('image_url', models.URLField(verbose_name='Image URL')),
            ],
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NoteHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticketmaster.eventhistory')),
            ],
        ),
        migrations.CreateModel(
            name='EventFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=False)),
                ('eventid', models.CharField(max_length=200, verbose_name='Event Name')),
                ('name', models.CharField(max_length=200, verbose_name='Event Name')),
                ('venue', models.CharField(max_length=200, verbose_name='Venue Name')),
                ('address', models.CharField(max_length=150, verbose_name='Venue Address')),
                ('city', models.CharField(max_length=150, verbose_name='Event City')),
                ('state', models.CharField(max_length=100, verbose_name='Event State')),
                ('start_date', models.CharField(max_length=100, verbose_name='Event Date')),
                ('start_time', models.CharField(max_length=100, verbose_name='Event Time')),
                ('ticket_link', models.URLField(verbose_name='Ticket Link')),
                ('image_url', models.URLField(verbose_name='Image URL')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]