from django.shortcuts import render
from datetime import datetime
from .models import *

CURRENT_YEAR_START = datetime.strptime('01/1/2019', '%m/%d/%Y').date()

# Create your views here.
def index(request):
    game_count = Game.objects.filter(finish_date__gte=CURRENT_YEAR_START).count()
    author_list = Author.objects.filter(game__finish_date__gte=CURRENT_YEAR_START).distinct('player')
    author_count = Author.objects.filter(game__finish_date__gte=CURRENT_YEAR_START).distinct('player').count()
    return render(request, 'backend/index.html', {'game_count': game_count,
                                                  'author_count': author_count,
                                                  'authors': author_list
                                                  })