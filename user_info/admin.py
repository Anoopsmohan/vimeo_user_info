from django.contrib import admin

from user_info.models import UserDetails

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'profile_url', 'paying', 'staff_pick', 'staff_pick_url', 'video_uploaded']
    search_fields = ['name']

admin.site.register(UserDetails, UserDetailsAdmin)
