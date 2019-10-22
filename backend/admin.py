from django.contrib import admin
from .models import Game, Team, Player, Personal_statistic, Rating, Code, Author

# Register your models here.
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Personal_statistic)
admin.site.register(Rating)
admin.site.register(Code)
admin.site.register(Author)