from django.shortcuts import render
from django.http import JsonResponse
from .util import query_graph_iri, query_graph_min


def home(request):
    sort_by = request.GET.get('sort')
    filter_by = request.GET.get('filter')

    random_books = query_graph_min(limit=3, is_random=True)
    books = query_graph_min(sort_by=sort_by, filter_by=filter_by)

    checked = "checked" if filter_by else ""
    return render(request, 'home.html', {'random_books': random_books, 'books': books, 'checked': checked})


def search_results(request):
    search_query = request.GET.get('query')
    sort_by = request.GET.get('sort')

    random_books = query_graph_min(limit=3, is_random=True)
    books = query_graph_min(title=search_query, author=search_query, sort_by=sort_by)

    query_get_parameters = "+".join(search_query.split())
    return render(request, 'search_results.html', {
        'query_result': books, 'query_param': query_get_parameters, 'random_books': random_books})


def book_detail(request, iri):
    book = query_graph_iri(iri)[0]
    return render(request, 'book_detail.html', {'book': book})


def load_more_books(request):
    query = request.GET.get('query')
    sort_by = request.GET.get('sort')
    offset = int(request.GET.get('offset'))
    limit = 12

    books = query_graph_min(title=query, author=query, sort_by=sort_by, offset=offset, limit=limit)
    end_of_data = False if len(books) == limit else True

    return JsonResponse({"books": books, "end_of_data": end_of_data})