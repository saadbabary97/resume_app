from requests import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, PostMedia


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['video', 'image', 'stickers']

class SUbPostSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['created_at', 'updated_at', 'media', 'is_subpost']

    def get_media(self, instance):
        media = PostMedia.objects.filter(subpost=instance).first()
        return  MediaSerializer(media).data
    #     subposts = []
    #     for media_file in instance.subpost_media_files.all():
    #         subpost = {
    #             'is_subpost': instance.is_subpost if instance.is_subpost is not None else "",
    #             'media': {
    #                 'video': media_file.video.url if media_file.video else "",
    #                 'image': media_file.image.url if media_file.image else "",
    #                 'stickers': media_file.stickers if media_file.stickers else "",
    #             }
    #         }
    #         subposts.append(subpost)
    #     return subposts

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['subpost'] = self.get_subpost(instance)
    #     return data



class PostSerializer(serializers.ModelSerializer):
    sub_post = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'created_at', 'updated_at', 'user', 'sub_post']

    def get_sub_post(self, instance):
        post_ids = PostMedia.objects.filter(post=instance).values_list('subpost', flat=True)
        sub_post = Post.objects.filter(id__in=post_ids)
        return SUbPostSerializer(sub_post, many=True).data