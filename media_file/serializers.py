from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PostMedia

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['image']

class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostMedia
        fields = ['video']

class StickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostMedia
        fields = ['stickers']
