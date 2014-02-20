__author__ = 'Iain'

from django.contrib import admin

from models import User, Game, Items, Inventory

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Items)
admin.site.register(Inventory)
