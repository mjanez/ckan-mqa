from controller.mqa_evaluate import mqa_evaluate
import os
import ssl
import sys

import requests
from requests.exceptions import HTTPError

from urllib.request import urlopen
import json

import rdflib

HYDRA = "http://www.w3.org/ns/hydra/core#"

OUTPUT = "local_evaluation"

def retrieve_hydra_value(graph, property):
    result = None
    hydra_type = rdflib.URIRef(HYDRA + "PagedCollection")
    for s, p, o in graph.triples((None, rdflib.namespace.RDF.type, hydra_type)):
        rdf_property = rdflib.term.URIRef(HYDRA + property)
        result = int(graph.value(s,rdf_property))
    return result

def parse_json_response(search_request, graph = None):
    """
    Parses the RDF contained as JSon response and adds it to the graph received as parameter
    """
    print(search_request)
    try:
        response = requests.get(search_request)
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        rdf_catalog = jsonResponse["result"]
        if graph is None:
            graph = rdflib.Graph()
        graph.parse(data=rdf_catalog,format="application/rdf+xml")
        return graph

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def catalog_search(ckan_url, file_name, keyword = 'test', serialization_format = 'turtle'):
    """
    Downloads the RDF in a paged JSON response
    """
    search_request = ckan_url + '/api/3/action/dcat_catalog_search?q='+keyword+'&format=rdf'
    graph = parse_json_response(search_request)

    items_per_page = retrieve_hydra_value(graph,'itemsPerPage')
    total_items = retrieve_hydra_value(graph,'totalItems')

    if (total_items > items_per_page):
        i = 2
        partial_count = items_per_page
        while (partial_count < total_items):
            search_request = ckan_url + '/api/3/action/dcat_catalog_search?q='+keyword+'&format=rdf&page='+str(i)
            parse_json_response(search_request,graph)
            partial_count = partial_count + items_per_page
            i = i + 1
    #graph.serialize(destination=file_name,format='pretty-xml')
    #graph.serialize(destination=file_name,format='turtle')
    graph.serialize(destination=file_name,format=serialization_format)

def package_search(ckan_url, file_name, keyword = 'test'):
    """
    Downloads the RDF in a paged JSON response with dataset identifiers
    """
    search_request = ckan_url + '/api/3/action/package_search?q='+keyword+'&rows=1000'
    print(search_request)
    try:
        response = urlopen(search_request)
        jsonResponse = json.load(response)
        rows = jsonResponse["result"]["results"]
        graph = rdflib.Graph()
        for row in rows:
            dataset_request = ckan_url + '/dataset/'+ row["name"] + '.rdf'
            print(dataset_request)
            graph.parse(dataset_request, format="application/rdf+xml")
        #graph.serialize(destination=file_name, format='pretty-xml')
        graph.serialize(destination=file_name, format='turtle')
    except Exception as err:
        print(f'Other error occurred: {err}')

def transform_to_file_name(url):
    x = ":/\\."
    y = "____"
    table = url.maketrans(x, y)
    return url.translate(table)

def create_folder(ckan_url):
    if (not os.path.exists(OUTPUT)):
        os.mkdir(OUTPUT)
    ckan_folder = transform_to_file_name(ckan_url)
    output_path = os.path.join(OUTPUT,ckan_folder)
    if (not os.path.exists(output_path)):
        os.mkdir(output_path)
    return output_path

def ckan_evaluation():
    ckan_url = 'http://localhost:5000'
    folder = create_folder(ckan_url)
    catalog_file_name = os.path.join(folder,'catalog.ttl')
    catalog_search(ckan_url, catalog_file_name)
    mqa_evaluate = mqa_evaluate(catalog_file_name, catalog_format= 'turtle')
    mqa_evaluate.evaluate()


if __name__ == '__main__':


    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    ckan_evaluation()

