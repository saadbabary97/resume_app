from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

        if self.image:
            try:
                image = Image.open(self.image.path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(self.image.path, format='JPEG', quality=20, optimize=True)
            except Exception as e:
                raise ValidationError(str(e))



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
class SharePost(models.Model):
    SHARE_REACTION_CHOICES = (
        ('like', 'Like'),
        ('haha', 'Haha'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_share")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_share")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    share_reaction = models.CharField(max_length=20, choices=SHARE_REACTION_CHOICES, null=True, default=None)
    share_comment =  models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        return f"{self.user.username} shared post {self.post.id}"

    class Meta:
        unique_together = ('user', 'post')

class UserFriends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_friend")
    requested_by = models.ManyToManyField(User, related_name="friend_requests", null=True
                                          )
    cancel_request = models.ManyToManyField(User, related_name="cancel_requests", null=True
                                            ) 
    friends = models.ManyToManyField(User, related_name="friends", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
