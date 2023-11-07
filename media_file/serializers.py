from requests import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, PostMedia, PostReaction, Comment, SharePost

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction_type')
class GetReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReaction
        fields = ['id', 'post', 'reaction_type']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id','user','post','comment_body','created_at', 'updated_at', 'username']

class PostShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = SharePost
        fields = ['post', 'created_at', 'updated_at', 'share_reaction', 'share_comment']
        
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['video', 'image', 'stickers']

class SubPostSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    sub_post_comments = serializers.SerializerMethodField()
    sub_post_reactions = serializers.SerializerMethodField()
    sub_post_share = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'created_at', 'updated_at', 'media', 'is_subpost', 'sub_post_comments', 'sub_post_reactions', 'sub_post_share']

    def get_media(self, instance):
        media = PostMedia.objects.filter(subpost=instance).first()
        return  MediaSerializer(media).data

    def get_sub_post_comments(self, instance):
        comments = Comment.objects.filter(post=instance)
        return CommentSerializer(comments, many=True).data

    def get_sub_post_reactions(self, instance):
        reactions = PostReaction.objects.filter(post=instance)
        return PostReactionSerializer(reactions, many=True).data
    
    def get_sub_post_share(self, instance):
        shares = SharePost.objects.filter(post=instance)
        print(shares)
        return PostShareSerializer(shares, many=True).data


class PostSerializer(serializers.ModelSerializer):
    sub_post = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    post_reaction_count = serializers.SerializerMethodField()
    share_post_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title', 'created_at', 'updated_at', 'comment_count', 'post_reaction_count', 'share_post_count', 'user', 'sub_post']

    def get_sub_post(self, instance):
        post_ids = PostMedia.objects.filter(post=instance).values_list('subpost', flat=True)
        sub_post = Post.objects.filter(id__in=post_ids)
        return SubPostSerializer(sub_post, many=True).data
    
    def get_user(self, instance):
        user = instance.user
        return {
            'first_name': user.first_name if user.first_name else None,
            'last_name': user.last_name if user.last_name else None,
        }

    def get_comment_count(self, instance):
        comment_count = Comment.objects.filter(post=instance).count()
        print('>><><><><><>><><>><><><><><><>',comment_count)
        return comment_count

    def get_post_reaction_count(self, instance):
        total_count = PostReaction.objects.all().count()
        print(total_count)
        post_reaction_count = PostReaction.objects.filter(post=instance).count()
        return post_reaction_count

    def get_share_post_count(self, instance):
        share_post_count = SharePost.objects.filter(post=instance).count()
        return share_post_count


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['post', 'comment_body', 'created_at', 'updated_at']
