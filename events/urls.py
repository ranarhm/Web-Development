from django.urls import path
from . import views
app_name = 'events'
urlpatterns = [
    # events_story views
    path('', views.home, name='home'),
    path('stories', views.events_story_list, name='story-list'),
    path('stories/<int:story_id>', views.events_story_detail, name='story-detail'),
    path('stories/add', views.create_event, name='create-event'),
    path('stories/new', views.event_added, name='event_added'),
    path('stories/results', views.search_results, name='search-results'),
    path('stories/results/none', views.search_results_none, name='search-results_none'),
    path('stories/edit/<int:story_id>', views.edit_event, name='edit'),
    path('stories/updated/<int:story_id>', views.event_changed, name='event_changed'),
    path('stories/delete/<int:story_id>', views.delete_event, name='delete'),
    path('stories/registered', views.events_story_registered, name='event_registered'),
    path('stories/liked', views.events_story_like, name='event_like'),
    path('stories/disliked', views.events_story_dislike, name='event_dislike'),
    path('stories/description', views.events_story_description, name='event_description'),
    path('stories/comments', views.view_comments, name='view_comments'),
    path('stories/comments/new', views.add_comment, name='add_comment'),
    path('stories/comments/edit/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('stories/comments/updated/<int:comment_id>', views.comment_changed, name='comment_changed'),
    path('stories/comment/delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('members', views.members, name='members'),
    path('contact', views.contact, name='contact'),
    path('media', views.media, name='media'),
    path('isvt', views.about, name='about'),
    path('directory', views.directory, name='directory'),
    path('join', views.join, name='join'),
    path('performer/facebook/<int:story_id>', views.performer_facebook, name='performer_facebook'),
    path('performer/facebook/added/<int:story_id>', views.performer_facebook_added, name='performer_facebook_added'),
]
