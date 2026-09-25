#File: forms.py
#Author: Niyoo Nedi (nnedi@bu.edu), 2/20/2026
#Description: File that contains the python for the creation of a post on the user side
    
from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''form to add a post to the database'''

    class Meta:
        '''associate this with a model from our DB'''

        model = Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):
    '''form to update a profile in the database'''

    class Meta:
        '''associate this with the model we are updating in our DB'''

        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text", "following", "followers"]


class UpdatePostForm(forms.ModelForm):
    '''form to update a post in the database'''

    class Meta:
        '''associate this with the model we are updating in our DB'''

        model = Post
        fields = ["caption"]


class ShowFollowersDetailView(forms.ModelForm):
    ''' a view to show a profile's followers'''

    model = Profile
    template_name = "mini_insta/show_followers.html" 
    context_object_name = "profile"


class ShowFollowingDetailView(forms.ModelForm):
    ''' a view to show a profile's following'''
    
    model = Profile 
    template_name = "mini_insta/show_following.html" 
    context_object_name = "profile"

class CreateProfileForm(forms.ModelForm):
    '''form for a user to create a new profile'''

    class Meta:
        '''associate this with the model we are updating in our DB'''
        model = Profile
        fields = ["username", "display_name", "profile_image_url", "bio_text", "followers", "following", "join_date"]
