from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Profile
from django.shortcuts import redirect
from .models import SavedPosts
from core.models import Post
from django.contrib import messages

# Create your views here.
@login_required(login_url='core:login')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    saved_post_list = SavedPosts.objects.filter(owner=user_profile)
    context = {
        'user_profile':user_profile,
        'saved_post_list':saved_post_list
    }
    return render(request,'saved_posts.html',context=context)

@login_required(login_url='core:login')
def save_post(request):
    user_profile = Profile.objects.get(user=request.user)
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    save_filter = SavedPosts.objects.filter(post=post,owner=user_profile).first()
    referrer = request.META.get('HTTP_REFERER')
    if save_filter == None:
        new_save = SavedPosts.objects.create(post=post,owner=user_profile)  
        new_save.save()
        return redirect(referrer)
    else:
        save_filter.delete()
        return redirect(referrer)