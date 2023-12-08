from django.shortcuts import render
from django.http import JsonResponse
import rdflib
from .util import query_graph

g = rdflib.Graph()
g.parse("static/data/Book_v2.ttl")


def home(request):
    sort_by = request.GET.get('sort')
    
    random_books = query_graph(g, limit=3, is_random=True)
    books = query_graph(g, sort_by=sort_by)

    return render(request, 'home.html', {'random_books': random_books, 'books': books})


def search_results(request):
    search_query = request.GET.get('query')
    sort_by = request.GET.get('sort')

    books = query_graph(g, title=search_query, author=search_query, sort_by=sort_by)

    query_get_parameters = "+".join(search_query.split())
    return render(request, 'search_results.html', {'query_result': books, 'query_param': query_get_parameters})


def book_detail(request):
    return render(request, 'book_detail.html')


def load_more_books(request):
    query = request.GET.get('query')
    sort_by = request.GET.get('sort')
    offset = int(request.GET.get('offset'))
    limit = 12

    books = query_graph(g, title=query, author=query, sort_by=sort_by, offset=offset, limit=limit)
    end_of_data = False if len(books) == limit else True

    return JsonResponse({"books": books, "end_of_data": end_of_data})
