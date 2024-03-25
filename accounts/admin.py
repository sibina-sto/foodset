# from django.contrib import admin
# from .models import Profile
#
# admin.site.register(Profile)

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     # list_display = ('user', 'image')
#     pass
# admin.site.register( Profile)

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')  # Customize the displayed fields in the list view

# admin.site.register(Profile, ProfileAdmin)
