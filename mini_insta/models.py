# File: models.py
# Author: Niyoo Nedi (nnedi@bu.edu), 2/13/2026
# Description: File that will contain the models for the mini_insta project

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''encapsulate the profile data'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    followers = models.IntegerField()
    following = models.IntegerField()
    join_date = models.DateTimeField(blank=True)

    def is_following(self, other_profile):
        '''helper function to see if a profile is following another'''
        return Follow.objects.filter(follower_profile=self, profile=other_profile).exists()

    def __str__(self):
        '''str rep of model instance'''
        return f'{self.username}'
    
    def get_all_posts(self):
        '''function that returns a query set of all of the posts for a specific profile'''

        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url(self):
        '''provide a url to redirect to after updating a profile'''

        return reverse('profile', kwargs={'pk':self.pk})
    
    def get_followers(self):
        '''gets the list of followers for a certain profile'''

        follows = Follow.objects.filter(profile=self)
        
        return [f.follower_profile for f in follows]
    
    def get_num_followers(self):
        '''gets the number of followers for a profile'''

        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        '''return a list of the Profiles followed by this profile'''

        follows = Follow.objects.filter(follower_profile=self)

        return [f.profile for f in follows]

    def get_num_following(self):
        '''count of how many profiles are being followed by a specific profile'''

        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        '''getting the post feed of a specific profile's instagram'''

        follows = Follow.objects.filter(follower_profile=self)
        followed_profiles = [f.profile for f in follows] 
        
        return Post.objects.filter(profile__in=followed_profiles).order_by('-timestamp')

    

class Post(models.Model):
    '''models the data attributes of an Instagram post'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''str rep of model instance'''
        return f'{self.caption, self.timestamp}'
    
    def get_all_photos(self):
        '''function that returns a query set of all of the photos for a specific post'''

        photos = Photo.objects.filter(post=self)
        return photos
    
    def display_image_url(self):
        '''function for displaying the photo''' 

        first_photo = self.photo_set.first() 

        if first_photo: 
            return first_photo.get_image_url()
        
        return "https://www.shutterstock.com/image-vector/error-500-page-empty-symbol-260nw-1711106146.jpg"
    
    def get_absolute_url(self):
        '''provide a url to redirect to after updating a profile'''
        
        return reverse('post', kwargs={'pk':self.pk})
    
    def get_all_comments(self): 
        ''' gets the comments on a post'''

        return Comment.objects.filter(post=self).order_by("timestamp")
    
    def get_likes(self):
        '''method to get all of the likes on a specific post'''

        likes = Like.objects.filter(post=self).count()
        return likes
    

class Photo(models.Model):
    '''models the data attributes of an Instagram post's photo'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(blank=True)

    image_file = models.ImageField(blank=True)

    def get_image_url(self):

        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url


    def __str__(self):
        '''str rep of model instance'''
        return f'{self.get_image_url(), self.timestamp}'
    

class Follow(models.Model):
    '''models the data attributes of an Instagram profile's followers'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        '''str rep of model instance'''
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"
    

class Comment(models.Model):
    '''models the data attributes of an Instragram post's comments'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        '''str rep of model instance'''
        return f"{self.profile.display_name} commented on Post {self.post.pk}"
    
    
class Like(models.Model):
    '''models the data attribubtes of an Instagram post's likes'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''str rep of model instance'''
        return f"{self.profile} liked {self.post}"
    



