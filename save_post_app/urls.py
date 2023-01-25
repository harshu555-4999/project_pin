from django.urls import path
from . import views

app_name = "saved"

urlpatterns = [
    path('',views.index,name='index'),
    path('save',views.save_post,name='save'),
]
