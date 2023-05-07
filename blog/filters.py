from django.contrib import admin
from django.db.models import Count

class CommentsCountFilter(admin.SimpleListFilter):
    title = 'comments count'
    parameter_name = 'comment'

    def lookups(self, request, model_admin):
        return [
            ('=0', 'Without comment'),
            ('0<', 'With comment')

        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(comments_count=Count('comment'))
        if self.value() == '=0':
            return annotated_value.filter(comments_count=0)
        elif self.value() == '0<':
            return annotated_value.filter(comments_count__gt=0)
        
class PostsCountFilter(admin.SimpleListFilter):
    title = 'posts count'
    parameter_name = 'post'

    def lookups(self, request, model_admin):
        return [
            ('=0', 'Without post'),
            ('0<', 'With post')

        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(posts_count=Count('post'))
        if self.value() == '=0':
            return annotated_value.filter(posts_count=0)
        elif self.value() == '0<':
            return annotated_value.filter(posts_count__gt=0)        