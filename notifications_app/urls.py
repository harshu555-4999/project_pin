from django.urls import path
from .views import index,read_notification

app_name = "notifications"

urlpatterns = [
    path('',index,name='index'),
    path('read/<not_id>',read_notification,name='read'),
]
