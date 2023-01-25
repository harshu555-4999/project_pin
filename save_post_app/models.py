from django.db import models

# Create your models here.
from django.db import models
from core.models import Profile,Post

# Create your models here.
class SavedPosts(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{} saved post {}'.format(self.owner.username,self.post.id)
