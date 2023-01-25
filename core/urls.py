from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    # path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.SearchView.as_view(), name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create', views.create, name='create'),
    path('bookmark-post', views.bookmark_post, name='bookmark-post'),
    path('post/<post_id>',views.post_detail,name='post-detail'),
]