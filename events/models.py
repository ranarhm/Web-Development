from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class EventsStory(models.Model):
    title = models.CharField(max_length=200)
    date_month = models.CharField(max_length=50)
    date_day = models.CharField(max_length=20)
    date_weekday = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    registered = models.IntegerField(default=0)
    description = models.TextField()
    performers = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:story-detail', args=[self.id])


class Comment(models.Model):
    title = models.CharField(max_length=200)
    comment = models.TextField()
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:view_comments')


# hard-coded user accounts
regular_user = {"username": "rana", "password": "regular"}
admin_user = {"username": "admin", "password": "admin"}


