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
        query = prefix+"""
    select ?judul_buku (group_concat(distinct ?nama_author; SEPARATOR=", ") AS ?authors) ?image where {{
        ?buku rdf:type :Book ;
            rdfs:label ?judul_buku ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?nama_author .
        
        filter(regex(?judul_buku, "{}", "i")||regex(?nama_author, "{}", "i"))
    }} group by ?judul_buku ?image
    """.format(input_get, input_get)
        
        
        try:
            result = g.query(query)
            query_result = process_query_result(result)
            return render(request, 'search_results.html', {'query_result': query_result})
        except Exception as e:
            print(e)

        return render(request, 'search_results.html')

    return render(request, 'search_results.html')

def book_detail(request):
    if request.method == 'GET':
        input_request = request.GET.get('data')
        input_iri_book = "<http://localhost:3333/data#{}>".format(input_request)
        
        query = prefix+"""
    select ?judul_buku (group_concat(distinct ?nama_author; SEPARATOR=", ") AS ?authors) ?image ?link ?publisher ?publish_date ?unit ?depth_value ?width_value ?length_value ?weight_value ?isbn ?avg_rating ?n_reviews where {{
        ?buku rdf:type :Book ;
            rdfs:label ?judul_buku ;
            prop:link ?link ;
            prop:image ?image ;
            prop:published_by ?published_by ;
            prop:publish_date ?publish_date ;
            prop:depth ?depth ;
            prop:width ?width ;
            prop:length ?length ;
            prop:weight ?weight ;
            prop:written_by ?author ;
            prop:isbn ?isbn ;
            prop:reviews ?reviews .
    
        ?published_by rdf:type :Publisher ;
            rdfs:label ?publisher .
        
        ?depth prop:unit ?unit ;
            prop:value ?depth_value .
        
        ?width prop:value ?width_value .
        
        ?length prop:value ?length_value .
        
        ?weight prop:value ?weight_value .
        
        ?author rdf:type :Author ;
            prop:name	?nama_author .
        
        ?reviews prop:avg_reviews ?avg_rating ;
            prop:n_reviews ?n_reviews .
        
        filter(?buku = {})
    }} group by ?judul_buku ?image ?link ?publisher ?publish_date ?unit ?depth_value ?width_value ?length_value ?weight_value ?isbn ?avg_rating ?n_reviews
    """.format(input_iri_book)
        
        try:
            result = g.query(query)
            detail_result = process_detail_result(result)
            return render(request, 'book_detail.html', {'detail_result': detail_result})
        except Exception as e:
            print(e)
        
        return render(request, 'book_detail.html')
    
    return render(request, 'book_detail.html')

def process_query_result(qres):
    list_of_dct = []

    for row in qres:
        dct = {}
        dct["judul_buku"] = row.judul_buku.toPython()
        dct["authors"] = row.authors.toPython()
        dct["image"] = row.image.toPython()

        list_of_dct.append(dct)
    
    return list_of_dct

def process_detail_result(res):
    dct = {}
    dct['judul_buku'] = res.judul_buku.toPython()
    dct["authors"] = res.authors.toPython()
    dct["link"] = res.link.toPython()
    dct["image"] = res.image.toPython()
    dct["publisher"] = res.publisher.toPython()
    dct["publish_date"] = res.publish_date.toPython()
    dct["unit"] = res.unit.toPython()
    dct["depth_value"] = res.depth_value.toPython()
    dct["width_value"] = res.width_value.toPython()
    dct["length_value"] = res.length_value.toPython()
    dct["weight_value"] = res.weight_value.toPython()
    dct["isbn"] = res.isbn.toPython()
    dct["avg_rating"] = res.avg_rating.toPython()
    dct["n_reviews"] = res.n_reviews.toPython()

    return dct