from .views import UserProfile
from django.urls import path
from. import views

urlpatterns = [
    path('profile/', views.UserProfile, name='user_profile'),
    path('profile/logout', views.exit_to_profile, name='profile_logout'),
]