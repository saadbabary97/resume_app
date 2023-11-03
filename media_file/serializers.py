from requests import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, PostMedia, PostReaction, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction_type')

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id','user','post','comment_body','created_at', 'updated_at', 'username']
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['video', 'image', 'stickers']

class SubPostSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    sub_post_comments = serializers.SerializerMethodField()
    sub_post_reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['created_at', 'updated_at', 'media', 'is_subpost', 'sub_post_comments', 'sub_post_reactions']

    def get_media(self, instance):
        media = PostMedia.objects.filter(subpost=instance).first()
        return  MediaSerializer(media).data

    def get_sub_post_comments(self, instance):
        comments = Comment.objects.filter(post=instance)
        return CommentSerializer(comments, many=True).data

    def get_sub_post_reactions(self, instance):
        reactions = PostReaction.objects.filter(post=instance)
        return PostReactionSerializer(reactions, many=True).data


class PostSerializer(serializers.ModelSerializer):
    sub_post = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'created_at', 'updated_at', 'user', 'sub_post']

    def get_sub_post(self, instance):
        post_ids = PostMedia.objects.filter(post=instance).values_list('subpost', flat=True)
        sub_post = Post.objects.filter(id__in=post_ids)
        return SubPostSerializer(sub_post, many=True).data