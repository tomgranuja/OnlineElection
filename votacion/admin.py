from django.contrib import admin
from .models import Profile, Vote, Election

# Register your models here.

admin.site.register(Profile)
admin.site.register(Vote)
admin.site.register(Election)
