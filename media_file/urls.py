from django.urls import path
from . import views

urlpatterns = [
    # Add the URL pattern for the get_posts view
    path('get_posts/', views.get_posts, name='get_posts'),
    path('create_post/', views.create_post, name='create_post'),

]
