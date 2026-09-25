# File: views.py
# Author: Niyoo Nedi (nnedi@bu.edu), 2/13/2026
# Description: File that will contain the view functions for the mini_insta project

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *
from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
import random
from django.utils import timezone

from .serializers import ProfileSerializer, PostSerializer, PhotoSerializer, UserSerializer


class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    '''overriding the default mixinclass'''
    login_url = "/mini_insta/login"

    def get_logged_in_profile(self):
        '''func to get logged in prof'''
        return Profile.objects.get(user=self.request.user)

# Create your views here.
class ProfileListView(ListView):
    '''define a view class to show all of the profile pages'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    '''define a view class to show one of the profile pages'''

    model = Profile
    template_name = "mini_insta/profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''get object function for viewing a profile, differentiating between whether pk is found or not'''

        if "pk" in self.kwargs:
            return super().get_object()
        
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        '''providing context variables for the view'''
        context = super().get_context_data(**kwargs)
        profile = context["profile"]

        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            context["is_following"] = Follow.objects.filter(follower_profile=logged_in_profile, profile=profile).exists()
        else:
            context["is_following"] = False

        return context
    

class PostDetailView(DetailView):
    '''defining a view class to show one of a profile's posts'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        '''providing the view with context data'''
        context = super().get_context_data(**kwargs)
        post = context["post"]

        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.get(user=self.request.user)
            context["is_liked"] = Like.objects.filter(profile=logged_in_profile, post=post).exists()
        else:
            context["is_liked"] = False

        return context


class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    '''defining a class view for a user to create a Post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'


    def get_success_url(self):
        '''provide a url to redirect to after creating a post'''

        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':pk})
    
    def get_context_data(self, **kwargs): 
        ''' providing context data for the view, feeding the pk'''
        context = super().get_context_data(**kwargs) 
        context['pk'] = self.kwargs['pk'] 
        return context
    

    def form_valid(self, form):
        '''handles form submission and adds the new post to the database and adds the foreign key of profile to the object'''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        response = super().form_valid(form)

        post = self.object
        
        # image_url = self.request.POST.get("image_url") 
        
        # if image_url: 
        #     Photo.objects.create(post=post, image_url=image_url, timestamp=form.cleaned_data['timestamp'])

        files = self.request.FILES.getlist('files') 
        
        for f in files: 
            Photo.objects.create( post=post, image_file=f, timestamp=form.cleaned_data['timestamp'] )
        
        return response


class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    ''' view class to handle the update of a profile accoridng to its PK'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        '''getting the profile that's logged in'''
        return Profile.objects.get(user=self.request.user)



class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView):
    ''' view class to update the update of a profile accoridng to its PK'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs): 
        '''function to define context variables for this view'''
        context = super().get_context_data(**kwargs) 
        
        post = self.get_object()
        profile = post.profile

        context['post'] = post
        context['profile'] = profile

        return context
    
    def get_success_url(self): 
        '''provide a url to redirect to after deleting a post'''

        post = self.get_object() 
        profile = post.profile

        return reverse("profile", kwargs={"pk": profile.pk})

    
class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView):
    ''' view class to update the update of a profile accoridng to its PK'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'


class ShowFollowersDetailView(DetailView):
    '''a view for the showing of a profile's followers'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    '''a view for the showing of a profile's following'''

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = "profile"


class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
    '''showing the list view of a profile's feed'''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = "posts"

    def get_context_data(self, **kwargs): 
        '''function to define context variables for this view'''
        
        context = super().get_context_data(**kwargs) 
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_queryset(self): 
        '''returning the list of posts that a certain profile should see on their feed'''
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()
    

class SearchView(MiniInstaLoginRequiredMixin, ListView):
    '''a view to handle the searching of profiles and posts'''

    template_name = 'mini_insta/search_results.html'
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        '''called to handle requests'''

        if "q" not in request.GET:
            profile = Profile.objects.get(user=self.request.user)
            return render(request, "mini_insta/search.html", {"profile": profile})
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''returning the list of posts that a contain the keywords in the query made by the user'''
        query = self.request.GET.get("q")
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        '''function to define context variables for this view'''

        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(user=self.request.user)
        query = self.request.GET.get("q")

        posts = context["posts"]

        profiles = (Profile.objects.filter(username__icontains=query) | Profile.objects.filter(display_name__icontains=query) | Profile.objects.filter(bio_text__icontains=query))

        context["profile"] = profile
        context["query"] = query
        context["profiles"] = profiles
        context["posts"] = posts

        return context


class CreateProfileView(CreateView):
    '''view  to handle the creation of a new profile'''
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        '''supplying the context data for the view'''
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''handles the form submission and adds the new profile to the db'''
        
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        
        return self.form_invalid(form)
    

class FollowView(MiniInstaLoginRequiredMixin, TemplateView):
    '''view that handles profile's following'''

    template_name = "mini_insta/profile.html"

    def dispatch(self, request, *args, **kwargs):
        '''called to handle requests'''
        logged_in_profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=kwargs["pk"])

        if logged_in_profile != other_profile:
            Follow.objects.get_or_create(follower_profile=logged_in_profile, profile=other_profile)

        return ProfileDetailView.as_view()(request, pk=other_profile.pk)
    

class DeleteFollowView(MiniInstaLoginRequiredMixin, TemplateView):
    '''view that handles profile's unfollowing'''

    template_name = "mini_insta/profile.html"

    def dispatch(self, request, *args, **kwargs):
        '''called to handle requests'''
        logged_in_profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=kwargs["pk"])

        Follow.objects.filter(follower_profile=logged_in_profile, profile=other_profile).delete()

        return ProfileDetailView.as_view()(request, pk=other_profile.pk)
    

class LikePostView(MiniInstaLoginRequiredMixin, TemplateView):
    '''view that handles the like of a post'''

    template_name = "mini_insta/show_post.html"

    def dispatch(self, request, *args, **kwargs):
        '''called to handle requests'''
        logged_in_profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(pk=kwargs["pk"])

        if post.profile != logged_in_profile:
            Like.objects.get_or_create(profile=logged_in_profile, post=post)

        view = PostDetailView.as_view()
        return view(request, pk=post.pk)
    

class DeleteLikePostView(MiniInstaLoginRequiredMixin, TemplateView):
    '''view that handles the unlike of a previously liked post'''
    template_name = "mini_insta/show_post.html"

    def dispatch(self, request, *args, **kwargs):
        '''called to handle requests'''
        logged_in_profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(pk=kwargs["pk"])

        Like.objects.filter(profile=logged_in_profile, post=post).delete()

        view = PostDetailView.as_view()
        return view(request, pk=post.pk)

#
#API VIEWS
#


class ListProfilesAPIView(APIView):
    '''Returns a list of profiles as JSON.'''
    #client must send Authorization Token header or they get 401
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''get function for this api view'''
        #gets the entire set of profiles and stores it in a variable
        profiles = Profile.objects.all()
        #putting the profile object into a serializer to be converted into json
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class SpecificProfileAPIView(APIView):
    '''Returns a specific Profile as JSON.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        '''get function for this api view'''
        #gets the specified profile and stores it in a variable
        profile = Profile.objects.get(pk=pk)
        #putting the profile object into a serializer to be converted into json
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    

class ProfilesPostAPIView(APIView):
    '''Returns a specific Profile's posts as JSON.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        '''get function for this api view'''
        #gets the specified profile and stores it in a variable
        profile = Profile.objects.get(pk=pk)
        #storing all of the posts from the specific profile
        posts = Post.objects.filter(profile=profile)
        #putting the posts into a serializer to be converted into json
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class ProfileFeedAPIView(APIView):
    '''Returns a specific profile's feed as JSON.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        '''get function for this api view'''
        #gets the specified profile and stores it in a variable
        profile = Profile.objects.get(pk=pk)
        #putting the feed into a serializer to be converted into json
        serializer = PostSerializer(profile.get_post_feed(), many=True)
        return Response(serializer.data)
    


class CreatePostAPIView(CreateAPIView):
    '''the api view for a post to be created'''
    #This tells DRF which serializer to use for validating and creating Post objects.
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        '''overwriting method to add extra fields that aren't given by client'''
        #getting the profile id from the URL
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        #make sure you can only create a post for your own profile not someone else's url
        if profile.user != self.request.user:
            raise PermissionDenied()
        #saving the new Post object and attaching it to the profile
        post = serializer.save(profile=profile)

        # Multipart posts omit image_url when only a file is sent; .get returns None.
        # URLField uses null=False, so None becomes a NOT NULL IntegrityError on SQLite.
        raw_url = self.request.data.get("image_url")
        image_url = (str(raw_url).strip() if raw_url is not None else "")
        image_file = self.request.FILES.get("image_file")

        #regardless of which format the user chose
        if image_url or image_file:
            #create a new photo object and specify the correct post, etc.
            Photo.objects.create(post=post, image_url=image_url, image_file=image_file, timestamp=timezone.now())


# views.py
from rest_framework import generics
from .serializers import UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    '''sign-up process, which allows new users to register themselves'''
    #specifies that UserSerializer will be used to validate and save the incoming user data
    serializer_class = UserSerializer


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserLoginView(APIView):
    '''setting up the Sign-In process, allowing users to authenticate and get a token'''
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        #used to verify user credentials against the database. 
        #Checks if username and password match and returns the user instance if successful
        user = authenticate(username=username, password=password)  # Authenticate the user
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)  # Create or retrieve a token for the user

            # find the profile connected to this user
            try:
                profile = Profile.objects.filter(user=user).first()
            except Profile.DoesNotExist:
                return Response({"error": "Profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'token': token.key, "profile_id": profile.id}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)



















