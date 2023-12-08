from django.urls import path
from .views import home, search_results, book_detail, load_more_books

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
    path('book/<str:iri>', book_detail, name='book_detail'),
    path('load_more_books/', load_more_books, name='load_more_books'),
]