from django.shortcuts import render
from datetime import datetime
from .models import *
from .sql_requests import *
import plotly.graph_objects as go

CURRENT_YEAR_START = datetime.strptime('01/1/2019', '%m/%d/%Y').date()

# Create your views here.
def index(request, year=2019):
    """
    games = Game.objects.filter(finish_date__gte=CURRENT_YEAR_START)
    game_count = Game.objects.filter(finish_date__gte=CURRENT_YEAR_START).count()
    author_list = Author.objects.filter(game__finish_date__gte=CURRENT_YEAR_START).distinct('player')
    author_count = Author.objects.filter(game__finish_date__gte=CURRENT_YEAR_START).distinct('player').count()
    a = get_count(year)
    print(a)"""
    games_count, authors_count, players_count, teams_count = get_count(year)
    max_resonance_game = get_resonance(year)
    max_quality_game = get_game_quality(year)
    print(type(max_quality_game))
    return render(request, 'backend/index.html', {'games_count': games_count,
                                                  'authors_count': authors_count,
                                                  'players_count': players_count,
                                                  'teams_count': teams_count,
                                                  'max_resonance_game': max_resonance_game

                                                  })