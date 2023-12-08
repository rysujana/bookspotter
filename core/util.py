from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper(
    "http://N-Slim7:7200/repositories/semweb"
)
sparql.setReturnFormat(JSON)

PREFIX = """
    prefix :      <http://localhost:3333/data#>
    prefix owl:   <http://www.w3.org/2002/07/owl#>
    prefix prop:  <http://localhost:333/property#>
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    prefix vcard: <http://www.w3.org/2006/vcard/ns#>
    prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
    """

def process_query_result(result):
    results = []

    for row in result["results"]["bindings"]:
        dct = {}
        for key, value in row.items():
            if key == "book_iri":
                iri = value["value"].split("#")[1]
                dct[key] = iri
            else:
                dct[key] = value["value"]

        results.append(dct)

    return results


def query_graph_min(title=None, author=None, sort_by=None, limit=12, offset=0, is_random=False):
    or_filters = []
    if title:
        title = title.replace('"', '\\"')
        title_query = f'regex(?title, "{title}", "i")'
        or_filters.append(title_query)
    else:
        title_query = ''

    if author:
        author = author.replace('"', '\\"')
        author_query = f'regex(?author_name, "{author}", "i")'
        or_filters.append(author_query)
    else:
        author_query = ''

    if sort_by == "title_asc":
        sorting_query = "order by ?title"
    elif sort_by == "title_desc":
        sorting_query = "order by desc(?title)"
    else:
        sorting_query = ""

    if is_random:
        sorting_query = "order by rand()"

    if len(or_filters) > 0:
        or_filters = " || ".join(or_filters)
        or_filters = f"filter({or_filters})"
    else:
        or_filters = ""

    query = PREFIX + f"""
    select distinct ?book_iri ?title (group_concat(distinct ?author_name; SEPARATOR=", ") AS ?authors) ?image
    where {{
        ?book_iri rdf:type :Book ;
            rdfs:label ?title ;
            prop:image ?image ;
            prop:written_by ?author .
        
        ?author rdf:type :Author ;
            prop:name ?author_name .
        {or_filters}
    }} group by ?book_iri ?title ?image
    {sorting_query}
    limit {limit}
    offset {offset}
    """

    sparql.setQuery(query)
    result = sparql.queryAndConvert()
    return process_query_result(result)


def query_graph_iri(iri):
    query = PREFIX + f"""
    select ?book_iri ?title (group_concat(distinct ?author_name; SEPARATOR=", ") AS ?authors) ?image ?link ?publisher ?publish_date ?dim_unit ?depth_value ?width_value ?length_value ?weight_unit ?weight_value ?isbn ?avg_rating ?n_reviews ?link ?price where {{
        ?book_iri rdf:type :Book ;
            rdfs:label ?title .
        
        optional {{
            ?book_iri prop:written_by ?author .
            ?author rdf:type :Author ;
                prop:name ?author_name .
        }} .
        optional {{ ?book_iri prop:link ?link }} .
        optional {{ 
            ?book_iri prop:published_by ?published_by .
            ?published_by rdf:type :Publisher ;
                rdfs:label ?publisher
        }} .
        optional {{ ?book_iri prop:publish_date ?publish_date }} .
        optional {{ 
            ?book_iri prop:depth [
                prop:unit ?dim_unit ;
                prop:value ?depth_value
            ] .    
        }} .
        optional {{ ?book_iri prop:width [ prop:value ?width_value ] }} .
        optional {{ ?book_iri prop:length [ prop:value ?length_value ] }} .
        optional {{ 
            ?book_iri prop:weight [
                prop:unit ?weight_unit ;
                prop:value ?wight_value
            ] .    
        }} .
        optional {{ ?book_iri prop:isbn ?isbn }} .
        optional {{ 
            ?book_iri prop:reviews [
                prop:avg_reviews ?avg_rating ;
                prop:n_reviews ?n_reviews
            ] 
        }} .
        optional {{ ?book_iri prop:image ?image }} .
        optional {{ 
            ?book_iri prop:price [
                prop:new_price ?price ;
            ] 
        }} .

        filter(?book_iri = :{iri})
    }} group by ?book_iri ?title ?image ?link ?publisher ?publish_date ?dim_unit ?depth_value ?width_value ?length_value ?weight_unit ?weight_value ?isbn ?avg_rating ?n_reviews ?link ?price
    """

    sparql.setQuery(query)
    result = sparql.queryAndConvert()
    return process_query_result(result)