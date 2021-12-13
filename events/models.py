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

# class EventsStory:
#     def __init__(self, id, title, date_month, date_day, score,
#                  author, author_name, host, registered, description, performers, role):
#         self.id = id
#         self.title = title
#         self.date_month = date_month
#         self.date_day = date_day
#         self.score = score
#         self.author = author
#         self.author_name = author_name
#         self.host = host
#         self.registered = registered
#         self.description = description
#         self.performers = performers
#         self.role = role
#
#
# story1 = EventsStory(
#     1,
#     "Distinguished Speaker Series: A Poetry Reading",
#     "OCT",
#     "01",
#     20,
#     "Created by ",
#     "Shabnam Moghadami",
#     "Hosted by ISVT",
#     "22 Registered",
#     "ISVT is proud to present the Distinguished Speaker Series: Dr. Mehrzad Boroujerdi on Prospects of US-Iran Relations, a live talk, and Q&A. The event will be held on Monday, Nov 16th at 7 pm via Zoom. Please submit your questions for Dr. Boroujerdi through the registration form attached below no later than Monday at 12 pm. Dr. Boroujerdi: Named Director of the School of Public and International Affairs at Virginia Tech, Dr. Mehrzaf Boroujerdi is an expert on Iran and Middle Eastern politics. He has authored more than 30 journal articles in English and Persian. He is the author of notable books such as Postrevolutionary Iran: A Political Handbook, Iranian Intellectuals, and the West: The Tormented Triumph of Nativism, and I Carved, Worshipped and Shattered: Essays on Iranian Politics and Identity. Dr. Boroujerdi has appeared on many national and international networks such as Al Jazeera, Associated Press, Guardian, LA Times, NPR, New York Times, Reuters, and Washington Post and is a regular commentator on many Persian broadcasting networks.",
#     "Dr. Mehrzad Boroujerdi",
#     "Director of the School of Public and International Affairs at Virginia Tech"
#
# )
#
# story2 = EventsStory(
#     2,
#     "Yalda Night Celebration",
#     "DEC",
#     "21",
#     28,
#     "Created by ",
#     "Mana Davari",
#     "Hosted by ISVT",
#     "16 Registered",
#     "Join us to party with D.J. Taba and celebrate the longest night of the year. There will be some translated Persian poetry (from the famous poet Hafez) to read if you want. You can bring your own Yalda-snacks and celebrate Yalda with us.",
#     "D.J. Taba",
#     "Radio Javan"
# )
#
# story3 = EventsStory(
#     3,
#     "Nowrouz - Persian New Year’s Eve Celebration",
#     "MAR",
#     "26",
#     50,
#     "Created by ",
#     "Arash Zamani",
#     "Hosted by ISVT",
#     "58 Registered",
#     "ISVT executive board would like to invite you all to our fourth event of the 2021-2022 academic year: Nowrouz. This event will be held to celebrate the Iranian new year which also coincides with the Spring vernal equinox. We will get together to have a wonderful night full of meet-and-greet, joy, happiness and fun. The event includes traditional Persian music, Stand-up comedy, Dance performance, dinner and dancing.",
#     "Rana Mansour رعنا منصور",
#     "Iranian-American singer"
# )
#
# events_stories = []
# events_stories.append(story1)
# events_stories.append(story2)
# events_stories.append(story3)


