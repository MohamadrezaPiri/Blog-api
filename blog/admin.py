from django.contrib import admin
from .models import Post,PostImage,Comment

# Register your models here.



class PostImageInline(admin.TabularInline):
    model=PostImage
    fields=['image']
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at','post_content']
    autocomplete_fields = ['user']
    search_fields = ['title']
    list_per_page=10
    inlines=[PostImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
