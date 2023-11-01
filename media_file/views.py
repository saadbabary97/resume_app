from django.shortcuts import render
from .models import Post, PostMedia
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

        serialized_posts.append({
            'title': post.title,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'user': {
                'username': post.user.username if post.user else None,
                'email': post.user.email if post.user else None,
            },
            'media': serialized_media
        })

    return JsonResponse({'posts': serialized_posts})


# Post request for Media files

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            title = post_data.get('title', '')
            user_data = post_data.get('user', {})

            user, created = User.objects.get_or_create(
                username=user_data.get('username', ''),
                email=user_data.get('email', '')
            )

            post = Post.objects.create(title=title, user=user)

            videos = post_data.get('videos', '')
            if videos and (videos.endswith(('.mp4', '.mov'))):
                PostMedia.objects.create(post=post, video=videos)

            images = post_data.get('images', [])
            # for image in images:
            if images.endswith(('.jpg', '.png', '.jpeg')):
                print('<image>:',images)
                PostMedia.objects.create(post=post, image=images)

            stickers = post_data.get('stickers', '')
            if stickers:
                PostMedia.objects.create(post=post, stickers=stickers)

            return JsonResponse({'message': 'Post created successfully'})
        except Exception as e:
            return HttpResponse({'error': str(e)}, status=500)
