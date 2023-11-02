from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True) 
    is_subpost = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to='media/videos/',null=True,blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv'])]
    )
    image = models.ImageField(upload_to='media/images/',null=True,blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    stickers = models.CharField(max_length=255, null=True, blank=True)
    subpost = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True, related_name='subpost_media_files')

    def __str__(self):
        return f"Media for Post: {self.post.title}"