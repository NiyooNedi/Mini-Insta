# File: urls.py
# Author: Niyoo Nedi (nnedi@bu.edu), 2/13/2026
# Description: File that will contain the urls for the mini_insta project

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

from django.urls import path
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),
    
    path('login/', auth_views.LoginView.as_view(template_name="mini_insta/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="show_all"), name="logout"),
    path('profile/', ProfileDetailView.as_view(), name='login_profile'),
    path("create_profile", CreateProfileView.as_view(), name="create_profile"),
    path("profile/<int:pk>/follow", FollowView.as_view(), name="follow"),
    path("profile/<int:pk>/delete_follow", DeleteFollowView.as_view(), name="delete_follow"),
    path("post/<int:pk>/like", LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/delete_like", DeleteLikePostView.as_view(), name="delete_like_post"),

    #path to register a new user over json api
    path("api/register/", UserRegistrationView.as_view(), name="api_register"),
    #path to log in and get a token and profile id back
    path("api/login/", UserLoginView.as_view(), name="api_login"),

    #path to list all profiles
    path("api/profiles/", ListProfilesAPIView.as_view(), name="api_profiles"),
    #path that gets one profile
    path("api/profile/<int:pk>/", SpecificProfileAPIView.as_view(), name="api_specific_profile"),
    #path that gets all posts posted one profile
    path("api/profile/<int:pk>/posts/", ProfilesPostAPIView.as_view(), name="api_profile_posts"),
    #path that gets a feed for one profile
    path("api/profile/<int:pk>/feed/", ProfileFeedAPIView.as_view(), name="api_profile_feed"),
    #path to create a post for one profile
    path("api/profile/<int:pk>/posts/create/", CreatePostAPIView.as_view(), name="api_create_post"),

]