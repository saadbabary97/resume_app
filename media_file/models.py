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
        return f"Media for Post: {self.post.title}---{self.subpost.id if self.subpost else None}"
class PostReaction(models.Model):
    REACTION_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('angry', 'Angry'),
        ('sad', 'Sad'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reactions")
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES,) 

    def __str__(self):
        return f"{self.user.username} reacted to post {self.post.id} with {self.reaction_type}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments", blank=True)
    comment_body = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment_body}-{self.user.username}"

    class Meta:
        ordering = ('-created_at',)