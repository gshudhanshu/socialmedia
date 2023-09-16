from django.contrib import admin
from .models import Post, Comment, Like


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)


# I wrote this code
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('content',)
    ordering = ('-created_at',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('user', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

# end of code I wrote
