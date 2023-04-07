from django.contrib import admin
from django.urls import reverse
from django.utils.html import urlencode, format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from .models import Post,PostImage,Comment

# Register your models here.



class PostImageInline(admin.TabularInline):
    model=PostImage
    fields=['image']
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at','post_content','comments_count']
    autocomplete_fields = ['user']
    search_fields = ['title']
    list_per_page=10
    inlines=[PostImageInline]

    def comments_count(self, post):
        url = (
            reverse('admin:blog_post_changelist')
            + '?'
            + urlencode({
                'post__id': str(post.id)
            }))
        return format_html('<a href="{}">{} comments</a>', url, post.comments_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            comments_count=Count('comment')
        )
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['user','post','content','date']
    autocomplete_fields=['user','post']
    search_fields=['user','content']
    list_per_page=10




admin.site.unregister(User)
user=get_user_model()



@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    search_fields=['username']
    fields=['username','first_name','last_name','email','password','is_staff','is_active']
    list_display=['username','first_name','last_name','email','is_staff']
    list_editable=['is_staff']
    list_per_page=10

    def posts_count(self, user):
        url = (
            reverse('admin:blog_post_changelist')
            + '?'
            + urlencode({
                'user__id': str(user.id)
            }))
        return format_html('<a href="{}">{} posts</a>', url, user.posts_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            posts_count=Count('post')
        )
    