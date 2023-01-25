from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100,default='No Name')
    id_user = models.PositiveIntegerField()
    bio = models.TextField(blank=True,max_length=500)
    profile_pic = models.ImageField(upload_to='profiles_images',default='default.png')
    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100, default='No name')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_bookmark = models.IntegerField(default=0)

    def __str__(self):
        return self.user




class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class BookmarkedPost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username