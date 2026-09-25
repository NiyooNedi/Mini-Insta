# File: serializers.py
# Author: Niyoo Nedi (nnedi@bu.edu), 4/9/2026
# Description: File that will contain the serializer classes for the mini_insta project

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import Post, Profile, Photo


class UserSerializer(serializers.ModelSerializer):
    '''serializer for registering through the api'''
    #password is write only so it doesnt go back in json
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    #create method customizes the user creation to handle password encryption correctly by using the create_user method
    def create(self, validated_data):
        '''create the django user with hashed password then make a Profile row that goes with them'''
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email") or "",
        )
        #also need a Profile or login cant look up profile_id
        Profile.objects.create(user=user, username=user.username, display_name=user.username, followers=0,following=0,join_date=timezone.now())
        return user


class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for the Profile model. Converts Profile objects to JSON and validates POST input.'''
    class Meta:
        #linkin the profile model to this class
        model = Profile
        #inputting the fields i want to be returned by to the api
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text']


class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for the Picture model. Converts Picture objects to JSON.'''
    image = serializers.SerializerMethodField()
    class Meta:
        #linking the Photo model to this class
        model = Photo
        #inputting the fields I want to be returned by to the api
        fields = ['id', 'post', 'image', 'timestamp']
    
    def get_image(self, photo):
        return photo.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    '''Serializer for the Post model. Converts Post objects to JSON.'''
    #calling on the photoserializer and storing it in a variable to pass into the fields variable
    photos = PhotoSerializer(source='photo_set', many=True, read_only=True)
    class Meta:
        #linking the Post model to this class
        model = Post
        #inputting the Post fields that I want to  be received by the client
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos']
        #readonly fields so the app only sends caption (and image_url handled in the view) not fake profile id
        read_only_fields = ['id', 'profile', 'timestamp', 'photos']










