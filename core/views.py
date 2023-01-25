from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, BookmarkedPost
from itertools import chain
import random
from core.forms import SignupForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetDoneView
from notifications_app.models import Notification
from save_post_app.models import SavedPosts

# Create your views here.

@login_required(login_url='core:login')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if 'searchQuerySubmit' in request.GET:
        q = request.GET.get('searchQueryInput')
        SearchView()

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

# @login_required(login_url='core:login')
# def upload(request):

#     if request.method == 'POST':
#         user = request.user.username
#         image = request.FILES.get('image_upload')
#         caption = request.POST['caption']

#         new_post = Post.objects.create(user=user, image=image, caption=caption)
#         new_post.save()

#         return redirect('/')
#     else:
#         return redirect('/')

# @login_required(login_url='core:login')
# def search(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=user_object)

#     if request.method == 'POST':
#         username = request.POST['searchQueryInput']
#         username_object = User.objects.filter(username__icontains=username)

#         username_profile = []
#         username_profile_list = []

#         for users in username_object:
#             username_profile.append(users.id)

#         for ids in username_profile:
#             profile_lists = Profile.objects.filter(id_user=ids)
#             username_profile_list.append(profile_lists)
        
#         username_profile_list = list(chain(*username_profile_list))
#     return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='core:login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    referrer = request.META.get('HTTP_REFERER')

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        user_obj = User.objects.get(username=post.user)
        user_profile = Profile.objects.get(user=user_obj)
        msg = str(username + " liked your post.")
        new_notification = Notification.objects.create(message=msg, user=user_profile)
        new_notification.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect(referrer)
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect(referrer)

@login_required(login_url='core:login')
def bookmark_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    bookmark_filter = BookmarkedPost.objects.filter(post_id=post_id, username=username).first()
    referrer = request.META.get('HTTP_REFERER')

    if bookmark_filter == None:
        new_bookmark = BookmarkedPost.objects.create(post_id=post_id, username=username)
        new_bookmark.save()
        post.no_of_bookmark = post.no_of_bookmark+1
        post.save()
        return redirect(referrer)
    else:
        bookmark_filter.delete()
        post.no_of_bookmark = post.no_of_bookmark-1
        post.save()
        return redirect(referrer)



@login_required(login_url='core:login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'


    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='core:login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            user_obj = User.objects.get(username=user)
            user_profile = Profile.objects.get(user=user_obj)
            msg = str(follower + " started following you.")
            new_notification = Notification.objects.create(message=msg, user=user_profile)
            new_notification.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='core:login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image-up')
        name = request.POST.get('fname').capitalize()
        bio = request.POST.get('bio').capitalize()

        user_profile.profile_pic = image
        user_profile.display_name = name
        user_profile.bio = bio
        user_profile.save()

        return redirect('core:index')
    return render(request, 'settings.html', {'user_profile': user_profile})

def signup(request):
    if 'login' in request.POST:
        return redirect("core:login")

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken!!!')
                return redirect('core:signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken!!!')
                return redirect('core:signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # messages.success(request, 'Your account has been successfully created!')
                new_notification = Notification.objects.create(message='Welcome to pinscribe!!!',user=new_profile)
                new_notification.save()
                
                return redirect('core:settings')
        else:
            messages.info(request, 'Confirmation password do not match!!!')
            return redirect('core:signup')
    else:
        return render(request, 'signup.html')

def login(request):
    if 'signup' in request.POST:
        return redirect("core:signup")
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password!!!')
            return redirect('core:login')

    else:
        return render(request, 'login.html')

@login_required(login_url='core:login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out!!!')
    return redirect('core:login')

@login_required(login_url='core:login')
def create(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if 'btn-back' in request.POST:
        return redirect('core:index')

    if request.method == 'POST':
        if request.FILES.get('post_image') != None:
            user = request.user.username
            image = request.FILES.get('post_image')
            caption = request.POST['caption'].capitalize()
            auth = user_profile.display_name

            new_post = Post.objects.create(user=user, image=image, caption=caption, author_name=auth)
            new_post.save()
            return redirect('/')
        else:
            messages.error(request,"Please select a file to upload before posting ;)")
            return render(request, 'upload.html',{'user_profile':user_profile})

    else:
        return render(request, 'upload.html',{'user_profile':user_profile})

class SearchView(ListView,LoginRequiredMixin):
    model = User
    template_name = 'search.html'
    context_object_name = 'username_profile_list'

    def get_queryset(self):
        username_profile_list = super(SearchView, self).get_queryset()
        query = self.request.GET.get('searchQueryInput')

        if self.request.GET.get('searchQueryInput') == None:
            postresult = User.objects.filter(username__iexact=self.request.user)
        else:
            postresult = User.objects.filter(username__contains=query)

        username_profile = []
        username_profile_list = []

        for users in postresult:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)     
        username_profile_list = list(chain(*username_profile_list))
        return username_profile_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context

@login_required(login_url='core:login')
def post_detail(request,post_id):
    post_obj = Post.objects.get(id=post_id)
    referrer = request.META.get('HTTP_REFERER')
    context = {
        'post':post_obj,
        'ref': referrer
    }
    return render(request,'post_detail.html',context=context)
