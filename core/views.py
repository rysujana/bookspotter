from django.shortcuts import render
from .models import Book
import rdflib

prefix = """\
    prefix :      <http://localhost:3333/data#> .
    prefix owl:   <http://www.w3.org/2002/07/owl#> .
    prefix prop:  <http://localhost:333/property#> .
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
    prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
    prefix xsd:   <http://www.w3.org/2001/XMLSchema#> . 
    """
g = rdflib.Graph()
g.parse("static/data/Book.ttl")

def home(request):
    return render(request, 'home.html')

def search_results(request):
    if request.method == 'GET':
        input_get = request.GET.get('query')
        print(input_get)
        dict_result = {}
        query = prefix+"""
            select ?judul_buku ?nama_author ?link where {{
                ?buku rdf:type :Book ;
                        rdfs:label ?judul_buku ;
                        prop:link ?link ;
                        prop:written_by ?author .
                
                ?author rdf:type :Author ;
                        prop:name	?nama_author .
                
                filter(regex(?judul_buku, "{}", "i")||regex(?nama_author, "{}", "i"))
            }}
            """.format(input_get, input_get)
        
        try:
            print("test")
            result = g.query(query)
            print(result)
        except (Exception):
            return "SPARQL Error!"

        return render(request, 'search_results.html')

    return render(request, 'search_results.html')

def book_detail(request):
    return render(request, 'book_detail.html')
