from django.contrib import admin

# Register your models here.
from .models import Post,Message,Profile,Comment,Like
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Like)
