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
    path('stories/edit/<int:story_id>', views.edit_event, name='edit'),
    path('stories/changed', views.event_changed, name='event_changed'),
    path('stories/delete/<int:story_id>', views.delete_event, name='delete'),
    path('stories/registered', views.events_story_registered, name='event_registered'),
    path('stories/comments', views.view_comment, name='view_comment'),
    path('stories/new-comment', views.add_comment, name='add_comment'),
    path('stories/comment/delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('members', views.members, name='members'),
]
