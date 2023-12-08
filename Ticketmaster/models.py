from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # favorites = models.ManyToManyField('EventFavorite', related_name='favorites', blank=True)
    def __str__(self):
        return self.user


class EventHistory(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventid = models.CharField('Event Name', max_length=200)
    name = models.CharField('Event Name', max_length=200)
    venue = models.CharField('Venue Name', max_length=200)
    address = models.CharField('Venue Address', max_length=150)
    city = models.CharField('Event City', max_length=150)
    state = models.CharField('Event State', max_length=100)
    start_date = models.CharField('Event Date',max_length=100)
    start_time = models.CharField('Event Time', max_length=100)
    ticket_link = models.URLField('Ticket Link', max_length=200)
    image_url = models.URLField('Image URL', max_length=200)

    def __str__(self):
        return self.name


class EventFavorite(models.Model):
    liked = models.BooleanField(default=False)
    eventid = models.CharField('Event Name', max_length=200)
    name = models.CharField('Event Name', max_length=200)
    venue = models.CharField('Venue Name', max_length=200)
    address = models.CharField('Venue Address', max_length=150)
    city = models.CharField('Event City', max_length=150)
    state = models.CharField('Event State', max_length=100)
    start_date = models.CharField('Event Date',max_length=100)
    start_time = models.CharField('Event Time', max_length=100)
    ticket_link = models.URLField('Ticket Link', max_length=200)
    image_url = models.URLField('Image URL', max_length=200)

    def __str__(self):
        return self.name


class NoteHistory(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventHistory, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.event} {self.message}"


# create profile for new users
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile, created = Userprofile.objects.get_or_create(user=instance)
        user_profile.user = instance
        user_profile.save()


post_save.connect(create_profile, sender=User)


