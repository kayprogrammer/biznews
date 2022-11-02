from django.contrib import admin

from . models import Article, Category, Comment, Reply

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'timestamp']
    list_filter = ['name']

    fieldsets = (
        ('General', {
            'fields': (
                'name', 'timestamp'
            ),
        }),
    )

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['admin', 'title', 'category', 'status', 'timestamp']
    list_filter = ['admin', 'title', 'category', 'featured', 'status', 'timestamp']
    readonly_fields = ['admin', 'views']

    fieldsets = (
        ('General', {
            'fields': (
                'admin', 'title', 'text', 'category', 'image'
            ),
        }),
        ('Checks', {
            'fields': (
                'featured', 'status', 'views', 'timestamp'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.admin = request.user
        obj.save()
        # super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'name', 'email', 'website']
    list_filter = ['article', 'name', 'email', 'website']

    fieldsets = (
        ('General', {
            'fields': (
                'article', 'name', 'email', 'website', 'message', 'timestamp'
            ),
        }),
    )

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['comment', 'name', 'email']
    list_filter = ['comment', 'name', 'email']

    fieldsets = (
        ('General', {
            'fields': (
                'comment', 'name', 'email', 'message', 'timestamp'
            ),
        }),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
