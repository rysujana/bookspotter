from django.shortcuts import render
from .models import Book

def home(request):
    return render(request, 'home.html')

def search_results(request):
    return render(request, 'search_results.html')

def book_detail(request):
    return render(request, 'book_detail.html')
