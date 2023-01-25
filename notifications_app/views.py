from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib.auth.models import User
from core.models import Profile
from django.shortcuts import redirect

# Create your views here.
@login_required(login_url='core:login')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    noti_list = Notification.objects.filter(user=user_profile,is_read=False)
    context = {
        'user_profile':user_profile,
        'noti_list':noti_list
    }
    return render(request,'notif.html',context=context)

@login_required(login_url='core:login')
def read_notification(request,not_id):
    noti_list = Notification.objects.get(not_id=not_id)
    noti_list.is_read = True
    noti_list.save()

    return redirect('notifications:index')
    