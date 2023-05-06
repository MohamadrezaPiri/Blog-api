from django.contrib import admin
from django.db.models import Count

class CommentsCountFilter(admin.SimpleListFilter):
    title = 'Comments'
    parameter_name = 'comments_count'

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