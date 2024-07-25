# third-party libraries
import rdflib
import rdflib.collection
import urllib.error
import logging

# custom functions
from config.log import get_log_module

HYDRA = "http://www.w3.org/ns/hydra/core#"


log_module = get_log_module()

def download_rdf(url, filename):
    """
    Downloads the file in url (intended to be the RDF end-point of a CKAN site) and stores it in filename
    """
    graph = rdflib.Graph()
    try:
        graph.parse(url, format="application/rdf+xml")
    except urllib.error.HTTPError as e:
        logging.error(f"{log_module}:Failed to parse URL {url}: {e}")
        return

    items_per_page = retrieve_hydra_value(graph, 'itemsPerPage')
    total_items = retrieve_hydra_value(graph, 'totalItems')
    if total_items > items_per_page:
        i = 2
        partial_count = items_per_page
        while partial_count < total_items:
            page_url = f"{url}?page={i}"
            try:
                graph.parse(page_url, format="application/rdf+xml")
                partial_count += items_per_page
                i += 1
            except urllib.error.HTTPError as e:
                logging.error(f"{log_module}:Failed to parse URL {page_url}: {e}")
                break
    graph.serialize(destination=filename,format='pretty-xml')

def retrieve_hydra_value(graph, property):
    result = None
    hydra_type = rdflib.URIRef(HYDRA + "PagedCollection")
    for s, p, o in graph.triples((None, rdflib.namespace.RDF.type, hydra_type)):
        rdf_property = rdflib.term.URIRef(HYDRA + property)
        result = int(graph.value(s,rdf_property))
    return result

