from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    # events_story views
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
    path('update/<str:username>', views.update_profile, name='update_profile'),
    path('edit/<str:username>', views.edit_profile, name='edit_profile'),
]
