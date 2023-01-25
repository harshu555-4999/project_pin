from django.db import models
from django.contrib.auth.models import User
from core.models import Profile

# Create your models here.
class Notification(models.Model):
    not_id = models.AutoField(primary_key=True)
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.message