from django.shortcuts import render
from django.http import JsonResponse
from .models import Book
import rdflib

prefix = """\
    prefix :      <http://localhost:3333/data#>
    prefix owl:   <http://www.w3.org/2002/07/owl#>
    prefix prop:  <http://localhost:333/property#>
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    prefix vcard: <http://www.w3.org/2006/vcard/ns#>
    prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
    """
g = rdflib.Graph()
g.parse("static/data/Book_v2.ttl")

def home(request):
    sort_by = request.GET.get('sort')
    
    random_query = prefix+"""
    select distinct ?book_iri ?title (group_concat(distinct ?author_name; SEPARATOR=", ") AS ?authors) ?image 
    where {
        ?book_iri rdf:type :Book ;
            rdfs:label ?title ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?author_name .
    } group by ?title ?image
    order by rand()
    limit 3
    """
    random_books = g.query(random_query)
    random_books = process_query_result(random_books)

    if sort_by == "title_asc":
        sorting_query = "order by ?title"
    elif sort_by == "title_desc":
        sorting_query = "order by desc(?title)"
    else:
        sorting_query = ""

    books_query = prefix+f"""
    select distinct ?book_iri ?title (group_concat(distinct ?author_name; SEPARATOR=", ") AS ?authors) ?image
    where {{
        ?book_iri rdf:type :Book ;
            rdfs:label ?title ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?author_name .
    }} group by ?title ?image
    {sorting_query}
    limit 12
    """
    books = g.query(books_query)
    books = process_query_result(books)

    return render(request, 'home.html', {'random_books': random_books, 'books': books})

def search_results(request):
    input_get = request.GET.get('query')

    query = prefix+"""
    select ?book_iri ?title (group_concat(distinct ?author_name; SEPARATOR=", ") AS ?authors) ?image 
    where {{
        ?book_iri rdf:type :Book ;
            rdfs:label ?title ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?author_name .
        
        filter(regex(?title, "{}", "i")||regex(?author_name, "{}", "i"))
    }} group by ?title ?image
    """.format(input_get, input_get)
    
    result = g.query(query)
    query_result = process_query_result(result)
    return render(request, 'search_results.html', {'query_result': query_result})


def book_detail(request):
    return render(request, 'book_detail.html')

def load_more_books(request):
    sort_by = request.GET.get('sort')
    offset = int(request.GET.get('offset'))
    limit = 12

    if sort_by == "title_asc":
        sorting_query = "order by ?title"
    elif sort_by == "title_desc":
        sorting_query = "order by desc(?title)"
    else:
        sorting_query = ""

    books_query = prefix+f"""
    select distinct ?book_iri ?title (group_concat(distinct ?author_name; SEPARATOR=", ") AS ?authors) ?image
    where {{
        ?book_iri rdf:type :Book ;
            rdfs:label ?title ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?author_name .
    }} group by ?title ?image
    {sorting_query}
    limit {limit}
    offset {offset}
    """
    books = g.query(books_query)
    books = process_query_result(books)

    end_of_data = False if len(books) == limit else True
    return JsonResponse({"books": books, "end_of_data": end_of_data})

def process_query_result(qres):
    list_of_dct = []

    for row in qres:
        dct = {}
        row = row.asdict()
        for key, value in row.items():
            if key == "book_iri":
                iri = value.toPython().split("#")[1]
                dct[key] = iri
            else:
                dct[key] = value.toPython()

        list_of_dct.append(dct)
    
    return list_of_dct

