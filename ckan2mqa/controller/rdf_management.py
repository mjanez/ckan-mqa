# third-party libraries
import rdflib
import rdflib.collection


HYDRA = "http://www.w3.org/ns/hydra/core#"

def download_rdf(url, filename):
    """
    Downloads the file in url (intended to be the RDF end-point of a CKAN site) and stores it in filename
    """
    graph = rdflib.Graph()
    graph.parse(url, format="application/rdf+xml")
    items_per_page = retrieve_hydra_value(graph,'itemsPerPage')
    total_items = retrieve_hydra_value(graph,'totalItems')
    if (total_items > items_per_page):
        i = 2
        partial_count = items_per_page
        while (partial_count < total_items):
            page_url = url+'&page='+str(i)
            graph.parse(page_url,format="application/rdf+xml")
            partial_count = partial_count + items_per_page
            i = i + 1
    graph.serialize(destination=filename,format='pretty-xml')

def retrieve_hydra_value(graph, property):
    result = None
    hydra_type = rdflib.URIRef(HYDRA + "PagedCollection")
    for s, p, o in graph.triples((None, rdflib.namespace.RDF.type, hydra_type)):
        rdf_property = rdflib.term.URIRef(HYDRA + property)
        result = int(graph.value(s,rdf_property))
    return result

