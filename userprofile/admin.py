from django.contrib import admin
from .models import UserProfile


# I wrote this code
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status_message', 'date_of_birth', 'status_updated_at')
    list_filter = ('user', 'date_of_birth', 'status_updated_at')
    search_fields = ('user', 'status_message', 'date_of_birth', 'status_updated_at')
    ordering = ('-status_updated_at',)


admin.site.register(UserProfile, UserProfileAdmin)

# end of code I wrote
