from django.urls import path
from . import views

urlpatterns = [
    # Add the URL pattern for the get_posts view
    path('get_posts/', views.get_posts, name='get_posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('get_single_post/<int:post_id>/', views.SinglePostView.as_view(), name='get_single_post'),
    path('create_post_reaction/', views.create_post_reaction, name='create_post_reaction'),
    path('update_post_reaction/', views.update_post_reaction, name='update_post_reaction'),

    path('create_comment/', views.create_comment, name='create_comment'),
    path('update_comment', views.update_comment, name='update_comment'),

    path('create_share/', views.create_share, name='create_share'),


    path('get_request/', views.GetFriendRequest.as_view(), name='get_request'),
    # path('get_suggestion/', views.GetSuggestions.as_view(), name='get_suggestion'),

    path('get_suggestion', views.suggest_friends, name='get_suggestion'),
    path('creata_request', views.friendrequestpost, name='creata_request'),
]
