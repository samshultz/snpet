from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = 'user', 'country', 'website', 'photo', 'last_login'
    list_filter = 'country',

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = "Last Login"

admin.site.register(Profile, ProfileAdmin)