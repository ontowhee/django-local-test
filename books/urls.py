from django.urls import path
from .views import index, create_book

app_name = 'books'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_book, name='create'),
]
