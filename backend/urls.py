from django.urls import path
from .views import index

urlpatterns = [
    path('index', index, name="index"),
    path('index/<int:year>/', index, name='index_year')
]