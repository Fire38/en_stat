from django.contrib import admin
from .models import Game, Team, Player

# Register your models here.
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Player)