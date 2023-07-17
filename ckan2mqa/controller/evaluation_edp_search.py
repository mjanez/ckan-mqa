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

OUTPUT = "edp"

def parse_dataset(id, graph):
    """
    Downloads the file in url (intended to be the RDF end-point of a CKAN site) and stores it in filename
    """
    ttl_url = 'https://www.europeandataportal.eu/data/api/datasets/'+ id + '.ttl?useNormalizedId=true&locale=en'
    print(ttl_url)
    try:
        graph.parse(ttl_url, format="turtle")
    except Exception as err:
        print(f'Other error occurred: {err}')
    return graph

def search(ckan_url, file_name, keyword = 'test'):
    """
    Downloads the RDF in a paged JSON response with dataset identifiers
    """
    search_request = ckan_url + '/search?q=%22'+keyword +'%22&limit=1000'
    print(search_request)
    try:
        response = urlopen(search_request)
        jsonResponse = json.load(response)
        rows = jsonResponse["result"]["results"]
        graph = rdflib.Graph()
        for row in rows:
            parse_dataset(row["id"],graph)
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

def edp_evaluation():
    ckan_url = 'https://www.europeandataportal.eu/data/search'
    folder = create_folder(ckan_url)
    catalog_file_name = os.path.join(folder,'catalog.ttl')
    search(ckan_url, catalog_file_name)
    mqa_evaluate = mqa_evaluate(catalog_file_name, catalog_format= 'turtle', catalog_type = 'edp')
    mqa_evaluate.evaluate()


if __name__ == '__main__':


    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    edp_evaluation()

