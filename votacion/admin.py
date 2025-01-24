from django.contrib import admin
from .models import Profile, Vote, Election

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = [ '__str__', 'voted', 'is_candidate' ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Vote)
admin.site.register(Election)
