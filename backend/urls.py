from django.urls import path
from .views import index, sql_requests

urlpatterns = [
    path('index', index, name='index'),
    path('index/<int:year>/', index, name='index_year'),
    path('sql_requests', sql_requests, name='sql_requests')
]