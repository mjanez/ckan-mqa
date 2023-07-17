from controller.mqa_evaluate import mqa_evaluate
from SPARQLWrapper import SPARQLWrapper, JSON

import os
import ssl

import rdflib

OUTPUT = "edp/"

EDP_SPARQL = 'https://www.europeandataportal.eu/sparql'

def get_file_name(url):
    """
    https://europeandataportal.eu/set/data/
    """
    words = url.split('/')
    file_name = words[len(words)-1]
    return file_name



def parse_dataset(url, graph):
    """
    Parses the dataset with URL in the graph
    """
    id = get_file_name(url)
    # https://www.europeandataportal.eu/data/api/datasets/https-opendata-aragon-es-datos-catalogo-dataset-oai-zaguan-unizar-es-94411.ttl?useNormalizedId=true&locale=en
    ttl_url = 'https://www.europeandataportal.eu/data/api/datasets/'+ id + '.ttl?useNormalizedId=true&locale=en'
    print(ttl_url)
    try:
        graph.parse(ttl_url, format="turtle")
    except Exception as err:
        print(f'Other error occurred: {err}')
    return graph

def parse_catalog(results, filename):
    graph = rdflib.Graph()
    for row in results["results"]["bindings"]:
        """s"""
        dataset = row["s"]["value"]
        graph = parse_dataset(dataset,graph)
    #graph.serialize(destination=filename, format='pretty-xml')
    graph.serialize(destination=filename, format='turtle')

def search_datasets_new(url, filename, keyword):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
          PREFIX dct:<http://purl.org/dc/terms/>
          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
          PREFIX dcat: <http://www.w3.org/ns/dcat#>
          SELECT DISTINCT ?s WHERE { 
            {  ?s a dcat:Dataset . 
               ?s dcat:keyword ?value . 
               FILTER regex(str(?value), '""" + keyword + """', 'i') 
            } UNION {
              ?s a dcat:Dataset . 
              ?s dct:description ?value . 
              FILTER regex(str(?value), '""" + keyword + """', 'i') 
            }
          }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    parse_catalog(results, filename)

def search_datasets(url, filename, keyword):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
          PREFIX dct:<http://purl.org/dc/terms/>
          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
          PREFIX dcat: <http://www.w3.org/ns/dcat#>
          SELECT DISTINCT ?s WHERE { 
          {  SELECT DISTINCT ?s WHERE {
               ?s a dcat:Dataset . 
               ?s dcat:keyword ?value . 
               FILTER regex(str(?value), '"""+ keyword +"""', 'i') .
               }
          } UNION {
            SELECT DISTINCT ?s WHERE { 
              ?s a dcat:Dataset . 
              ?s dct:description ?value . 
              FILTER regex(str(?value), '"""+ keyword + """', 'i') .
              }
          }
          }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    parse_catalog(results,filename)


def search_datasets_with_publisher(url, filename, keyword, publisher):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
          PREFIX dct:<http://purl.org/dc/terms/>
          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
          PREFIX dcat: <http://www.w3.org/ns/dcat#>
          SELECT DISTINCT ?s WHERE { 
            { 
               ?s a dcat:Dataset . 
               ?s dcat:keyword ?value . 
               FILTER regex(str(?value), '"""+ keyword +"""', 'i') . 
               ?s dct:publisher <""" + publisher + """> 
            } UNION {
               ?s a dcat:Dataset . 
               ?s dct:description ?value . 
               FILTER regex(str(?value), '"""+ keyword + """', 'i') . 
               ?s dct:publisher <""" + publisher + """> 
            }
          }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    parse_catalog(results,filename)


def search_datasets_example_endpoint(url, filename, keyword):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
          PREFIX dct:<http://purl.org/dc/terms/>
          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
          PREFIX dcat: <http://www.w3.org/ns/dcat#>
          PREFIX foaf: <http://xmlns.com/foaf/0.1/>
          SELECT DISTINCT ?s WHERE { 
          {  
               ?s a dcat:Dataset . 
               ?s dcat:keyword ?value . 
               FILTER regex(str(?value), '"""+ keyword +"""', 'i') . 
               ?s foaf:page ?page .
          } UNION {
               ?s a dcat:Dataset . 
               ?s dct:description ?value . 
               FILTER regex(str(?value), '"""+ keyword + """', 'i') . 
               ?s foaf:page ?page .
          } UNION {
               ?s a dcat:Dataset . 
               ?s dct:description ?value . 
               FILTER regex(str(?value), '"""+ keyword + """', 'i') . 
               ?s dct:rightsHolder ?rh .
               ?rh dct:identifier ?id .
               FILTER(str(?id)='r_toscan') . 
          } UNION {
               ?s a dcat:Dataset . 
               ?s dct:description ?value . 
               FILTER regex(str(?value), '"""+ keyword + """', 'i') . 
               ?s dct:rightsHolder ?rh .
               ?rh dct:identifier ?id .
               FILTER(str(?id)='r_toscan') . 
          }
          }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    parse_catalog(results,filename)


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
    folder = create_folder('edp_all')
    catalog_file_name = os.path.join(folder,'catalog.ttl')
    search_datasets(EDP_SPARQL, catalog_file_name, 'MNR')
    mqa_evaluate = mqa_evaluate(catalog_file_name, catalog_format= 'turtle', catalog_type = 'edp')
    mqa_evaluate.evaluate()

def edp_minint_evaluation():
    folder = create_folder('edp_mnr')
    catalog_file_name = os.path.join(folder,'catalog.ttl')
    publisher = 'http://datos.gob.es/recurso/sector-publico/org/Organismo/E00003801' ## Ministerio del Interior de España
    search_datasets_with_publisher(EDP_SPARQL, catalog_file_name, 'MNR', publisher)
    mqa_evaluate = mqa_evaluate(catalog_file_name, catalog_format= 'turtle', catalog_type = 'edp')
    mqa_evaluate.evaluate()

if __name__ == '__main__':

    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    edp_minint_evaluation()
    edp_evaluation()
