# instaclone/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('feed/', views.feed_view, name='feed'),
    path('create_post/', views.create_post_view, name='create_post'),
    path('update_post/<int:post_id>/', views.update_post_view, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post_view, name='like_post'),
    path('comment_post/<int:post_id>/', views.comment_post_view, name='comment_post'),
    
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile_view, name='update_profile'),
    path('delete_profile/', views.delete_profile_view, name='delete_profile'),
    
    path('chat/', views.chat_list_view, name='chat_list'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('send_message/<str:username>/', views.send_message_view, name='send_message'),
]