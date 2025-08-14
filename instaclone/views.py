from django.shortcuts import render

# Create your views here.
# instaclone/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Profile, Post, Like, Comment, Message
from django.utils import timezone

# instaclone/views.py
def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'welcome.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect('feed')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

@login_required
def create_post_view(request):
    if request.method == 'POST':
        image = request.FILES['image']
        caption = request.POST['caption']
        post = Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('feed')
    return render(request, 'create_post.html')

@login_required
def update_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.caption = request.POST['caption']
        post.save()
        return redirect('feed')
    return render(request, 'update_post.html', {'post': post})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('feed')

@login_required
@require_POST
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
    
    return JsonResponse({'likes_count': post.like_set.count(), 'liked': created})

@login_required
@require_POST
def comment_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST['text']
    comment = Comment.objects.create(user=request.user, post=post, text=text)
    return JsonResponse({
        'success': True,
        'comment': {
            'text': comment.text,
            'username': comment.user.username,
            'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p')
        }
    })

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts})

@login_required
def update_profile_view(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.bio = request.POST['bio']
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'update_profile.html', {'profile': profile})

@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login')
    return render(request, 'delete_profile.html')

@login_required
def chat_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat_list.html', {'users': users})

from django.db import models  # Add this import at the top

@login_required
def chat_view(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=receiver) |
        models.Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages
    })

@login_required
@require_POST
def send_message_view(request, username):
    receiver = get_object_or_404(User, username=username)
    text = request.POST['text']
    message = Message.objects.create(sender=request.user, receiver=receiver, text=text)
    return JsonResponse({
        'success': True,
        'message': {
            'text': message.text,
            'timestamp': message.timestamp.strftime('%b %d, %Y %I:%M %p')
        }
    })