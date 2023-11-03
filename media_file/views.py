from django.shortcuts import render
from media_file.serializers import PostMedia, PostSerializer
from .models import Post, PostMedia, PostReaction, Comment
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Get request for Media files
def get_posts(request):
    posts = Post.objects.all()
    serialized_posts = []

    for post in posts:
        serialized_media = []
        for media in PostMedia.objects.filter(post=post):
            serialized_media.append({
                'video': media.video.url if media.video else None,
                'image': media.image.url if media.image else None,
                'stickers': media.stickers,
            })

        reactions = PostReaction.objects.filter(post=post)
        comments = Comment.objects.filter(post=post)

        serialized_posts.append({
            'title': post.title,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'is_subpost': post.is_subpost,
            'user': {
                'username': post.user.username if post.user else None,
                'email': post.user.email if post.user else None,
            },
            'media': serialized_media,
            'reactions': [{'user': reaction.user.username, 'reaction_type': reaction.reaction_type} for reaction in reactions],
            'comments': [{'user': comment.user.username, 'comment_body': comment.comment_body} for comment in comments],
        })

    return JsonResponse({'posts': serialized_posts})



# Get request for Single Post
class SinglePostView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Post request for Media files

@api_view(['POST'])
@permission_classes([AllowAny])
def create_post(request):
    try:
        post_data = request.data
        images = post_data.getlist('images', [])
        videos = post_data.getlist('videos', [])
        stickers = post_data.get('stickers', '')
        username = request.POST.get('user[username]', '')
        email = request.POST.get('user[email]', '')
        title = post_data.get('title', '')
        is_subpost = post_data.get('is_subpost', False)
        print('title:',title)
        print('username:',username)
        print('email:',email)
        print('Videos:', videos)
        print('Images:',images)

        user, created = User.objects.get_or_create(username=username, email=email)

        post = Post.objects.create(title=title, user=user, is_subpost=is_subpost)

        serialized_objects = []
        if video > 1:
            for video in videos:
                subpost = Post.objects.create(user=user, is_subpost=True)
                post_video = PostMedia.objects.create(video=video, post=post, subpost=subpost)
                serializer = PostMedia(post_video)
                serialized_objects.append(serializer.data)
        if image > 1:
            for image in images:
                subpost = Post.objects.create(is_subpost=True, user=user)
                post_image = PostMedia.objects.create(image=image, post=post, subpost=subpost)
                serializer = PostMedia(post_image)
                serialized_objects.append(serializer.data)

        if stickers:
            PostMedia.objects.create(post=post, stickers=stickers)

        if is_subpost:
            subpost_data = post_data.get('subpost', {})
            subpost = Post.objects.create(title=subpost_data.get('title', ''), user=user, is_subpost=True)
            PostMedia.objects.create(post=post, subpost=subpost)

        return JsonResponse({'message': serialized_objects})
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(str(e))

        return JsonResponse({'error': str(e)}, status=500)