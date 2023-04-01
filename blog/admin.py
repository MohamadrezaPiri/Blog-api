from django.contrib import admin
from .models import Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at','post_content']
    autocomplete_fields = ['user']
    search_fields = ['title']
    list_per_page=10