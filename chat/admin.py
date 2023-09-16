from django.contrib import admin
from .models import ChatRoom, ChatMessage


# I wrote this code
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    ordering = ('-created_at',)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'user', 'message', 'created_at')
    list_filter = ('room_name', 'user', 'created_at')
    search_fields = ('room_name', 'user', 'message', 'created_at')
    ordering = ('-created_at',)


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)

# end of code I wrote
