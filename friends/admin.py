from django.contrib import admin
from .models import *


# I wrote this code
class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'accepted', 'created_at', 'accepted_at')
    list_filter = ('accepted', 'created_at', 'accepted_at')
    search_fields = ('user', 'friend', 'accepted', 'created_at', 'accepted_at')


admin.site.register(Friend, FriendAdmin)

# end of code I wrote
