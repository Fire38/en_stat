from django.contrib import admin
from .models import Game, Team, Player, Personal_statistic

# Register your models here.
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Personal_statistic)