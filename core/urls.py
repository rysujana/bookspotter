from django.urls import path
from .views import home, search_results, book_detail

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
    path('book/1/', book_detail, name='book_detail'),
]