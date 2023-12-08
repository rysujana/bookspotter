from django.shortcuts import render
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
    return render(request, 'home.html')

def search_results(request):
    if request.method == 'GET':
        input_get = request.GET.get('query')
        print(input_get)
        dict_result = {}
        query = prefix+"""
    select ?judul_buku ?nama_author ?image where {{
        ?buku rdf:type :Book ;
            rdfs:label ?judul_buku ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?nama_author .
        
        filter(regex(?judul_buku, "{}", "i")||regex(?nama_author, "{}", "i"))
    }}
    """.format(input_get, input_get)
        
        
        try:
            print("test")
            print(query)
            result = g.query(query)
            print(result)
            context = process_query_result(result)
            return render(request, 'search_results.html', context)
        except (Exception):
            print("Error")

        return render(request, 'search_results.html')

    return render(request, 'search_results.html')

def book_detail(request):
    return render(request, 'book_detail.html')

def process_query_result(qres):
    list_of_dct = []

    for row in qres:
        dct = {}
        dct["judul_buku"] = row.judul_buku.toPython()
        dct["nama_author"] = row.nama_author.toPython()
        dct["image"] = row.image.toPython()

        list_of_dct.append(dct)
    
    return list_of_dct

