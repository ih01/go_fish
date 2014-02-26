__author__ = 'Iain'
from django.contrib import admin
from models import UserProfile, Game, Rod, Boat, Bait
admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Rod)
admin.site.register(Boat)
admin.site.register(Bait)
