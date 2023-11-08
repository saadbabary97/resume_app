from django.shortcuts import render
from media_file.serializers import PostMedia, PostSerializer, PostReactionSerializer, PostCommentSerializer, PostShareSerializer, MediaSerializer, FriendRequestSerializer
from .models import Post, PostMedia, PostReaction, Comment, SharePost, UserFriends
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

# Get request for Media files

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    posts = Post.objects.filter(user=request.user, is_subpost = False)
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
        shares = SharePost.objects.filter(post=post)

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
            'shares':[{'user':share.user.username, 'share_reaction': share.share_reaction, 'share_comment': share.share_comment} for share in shares]
        })

    return Response({'posts': serialized_posts})



# Get request for Single Post
class SinglePostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Post request for Media files

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
        if videos:
            for video in videos:
                if video.size > 1:
                    subpost = Post.objects.create(user=user, is_subpost=True)
                    post_video = PostMedia.objects.create(video=video, post=post, subpost=subpost)
                    serializer = MediaSerializer(post_video)
                    serialized_data = serializer.data
                    serialized_objects.append(serialized_data)
        if images:
            for image in images:
                if image.size > 1:
                    subpost = Post.objects.create(is_subpost=True, user=user)
                    post_image = PostMedia.objects.create(image=image, post=post, subpost=subpost)
                    serializer = MediaSerializer(post_image)
                    serialized_data = serializer.data  
                    serialized_objects.append(serialized_data)


        if stickers:
            PostMedia.objects.create(post=post, stickers=stickers)

        if is_subpost:
            subpost_data = post_data.get('subpost', {})
            subpost = Post.objects.create(title=subpost_data.get('title', ''), user=user, is_subpost=True)
            PostMedia.objects.create(post=post, subpost=subpost)

        return JsonResponse({'message': serialized_objects})
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(str(e))
        traceback.print_exc() 
        return JsonResponse({'error': str(e)}, status=500)
    
#Post for Reaction
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_post_reaction(request):
    user = request.user
    post_id = request.data.get('post_id')
    reaction_type = request.data.get('reaction_type')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        post_reaction = PostReaction.objects.create(user=user, post=post, reaction_type=reaction_type)
        serializer = PostReactionSerializer(post_reaction)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#Patch for Reaction
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_post_reaction(request):
    user = request.user
    post_id = request.data.get('post_id')
    reaction_type = request.data.get('reaction_type')

    try:
        post_reaction = PostReaction.objects.get(user=user, post__id=post_id)
        post_reaction.reaction_type = reaction_type
        post_reaction.save()
        serializer = PostReactionSerializer(post_reaction)
        return Response(serializer.data)
    except PostReaction.DoesNotExist:
        return Response({'error': 'Post reaction does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Post Comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    user = request.user
    comment_id = request.data.get('comment_id')
    comment_body = request.data.get('comment_body')
    print('comment_id',comment_id)
    print('comment_body',comment_body)

    post = Post.objects.get(id=comment_id)
    print("post....",post)
    try:
        post_comment = Comment.objects.create(user=user, post=post, comment_body=comment_body)
        serializer = PostCommentSerializer(post_comment)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#Patch Comment
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_comment(request):
    user = request.user
    comment_id = request.data.get('comment_id')
    comment_body = request.data.get('comment_body')
    try:
        print(">...>>>>>>>>>>>>>>.............>>>>>>>>>>>...........>>>>>>>>>>.........>>>>>>>")
        post_comment = Comment.objects.get(user=user ,post__id=comment_id)
        print('post comment:..',post_comment)
        post_comment.comment_body = comment_body
        post_comment.save()
        serializer = PostCommentSerializer(post_comment)
        print("Serializer Data: ",serializer)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Post Share
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_share(request):
    user = request.user
    share_id = request.data.get('share_id')
    share_reaction = request.data.get('share_reaction')
    share_comment = request.data.get('share_comment')

    print("Share ID:....",share_id)

    post_share_id = Post.objects.get(id=share_id)
    try:
        post_share = SharePost.objects.create(user=user, post=post_share_id, share_reaction=share_reaction, share_comment=share_comment)
        serializer = PostShareSerializer(post_share)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


#Sinlge Api for Reaction count
class GetFriendRequest(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            user = request.user
            print(user)
            friend_request_users = UserFriends.objects.filter(user=user)
            print(friend_request_users)
            serializer = FriendRequestSerializer(friend_request_users, many=True)
            print(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def friendrequestpost(request):
    user = request.user
    requested_by_id = request.data.get('requested_by',)
    cancel_request_id = request.data.get('cancel_request',)
    friends_id = request.data.get('friends',)

    user_friends, created = UserFriends.objects.get_or_create(user=user)

    if requested_by_id:
        try:
            requested_by_user = User.objects.get(id=requested_by_id)
            user_friends.requested_by.add(requested_by_user)
        except User.DoesNotExist:
            return Response({'error': 'Requested user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if cancel_request_id:
        try:
            cancel_request_user = User.objects.get(id=cancel_request_id)
            user_friends.cancel_request.add(cancel_request_user)
        except User.DoesNotExist:
            return Response({'error': 'Cancel request user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    if friends_id:
        try:
            friends_user = User.objects.get(id=friends_id)
            user_friends.friends.add(friends_user)
        except User.DoesNotExist:
            return Response({'error':'Friend user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = FriendRequestSerializer(user_friends)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggest_friends(request):
    user = request.user
    suggestions = []

    user_friends, created = UserFriends.objects.get_or_create(user=user)

    if user_friends:
        friends_id = user_friends.friends.values_list('id', flat=True)
        print("friends_id:",friends_id)
        requested_by_id = user_friends.requested_by.values_list('id', flat=True)
        print("requested_by_id:",requested_by_id)
        cancel_request_id = user_friends.cancel_request.values_list('id', flat=True)
        print("cancel_request_id:",cancel_request_id)

        users_to_exclude = list(friends_id) + list(requested_by_id) + list(cancel_request_id) + [user.id]
        print("users_to_exclude:",users_to_exclude)

        suggested_users = User.objects.filter(is_active=True).exclude(id__in=users_to_exclude)
        print("suggested_users:",suggested_users)

        suggestions = [{'id': user.id, 'username': user.username} for user in suggested_users]

    return Response(suggestions)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggest_friends(request):
    user = request.user
    suggestions = []

    user_friends, created = UserFriends.objects.get_or_create(user=user)

    if user_friends:
        
        friends_id = user_friends.friends.values_list('id', flat=True)
        print("friends_id:",friends_id)
        requested_by_id = user_friends.requested_by.values_list('id', flat=True)
        print("requested_by_id:",requested_by_id) 
        cancel_request_id = user_friends.cancel_request.values_list('id', flat=True)
        print("cancel_request_id:",cancel_request_id)
        
        exclusion_conditions = Q(id__in=friends_id) | Q(id__in=requested_by_id) | Q(id__in=cancel_request_id) | Q(id=user.id)
        print("users_to_exclude:",exclusion_conditions)
        
        suggested_users = User.objects.filter(is_active=True).exclude(exclusion_conditions)
        print("suggested_users:",suggested_users)
        
        suggestions = [{'id': user.id, 'username': user.username} for user in suggested_users]

    return Response(suggestions)
