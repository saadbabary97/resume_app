from django.urls import path
from . import views


urlpatterns = [
    path('portfolio/<int:portfolio_id>/', views.portfolio_detail, name='portfolio-detail'),
    path('create_portfolio', views.create_portfolio, name='create_portfolio'),
    path('update_portfolio/<int:portfolio_id>/', views.update_portfolio, name='update-portfolio'),

    #Education Api
    path('create_education', views.create_education, name='create_education'),
    path('update_education/<int:id>/', views.update_education, name='update_education'),
    path('delete_education/<int:id>/', views.delete_education, name='delete_education'),

    #Skill Api
    path('create_skill', views.create_skill, name='create_skill'),
    path('update_skill/<int:id>/', views.update_skill, name='update_skill'),
    path('delete_skill/<int:id>/', views.delete_skill, name='delete_skill'),

    #Hobby Api
    path('create_hobby', views.create_hobby, name='create_hobby'),
    path('update_hobby/<int:id>/', views.update_hobby, name='update_hobby'),
    path('delete_hobby/<int:id>/', views.delete_hobby, name='delete_hobby'),


    #Experience Api
    path('create_experience', views.create_experience, name='create_experience'),
    path('update_experience/<int:id>/', views.update_experience, name='update_experience'),
    path('delete_experience/<int:id>/', views.delete_experience, name='delete_experience'),


]
