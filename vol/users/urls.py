from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'), 
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),
    path('profile/<slug:slug>', views.Profile.as_view(), name='profile'),
    path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('update_rating/<slug:slug>', views.UpdateRating.as_view(), name='update_rating'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('teamform', views.create_team, name='teamform'),
    path('teams', views.TeamList, name='teams'),
    path('team/<int:pk>', views.TeamDetail, name='team_detail')
    ]
