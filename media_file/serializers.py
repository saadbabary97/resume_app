from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PostMedia

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('image',)

