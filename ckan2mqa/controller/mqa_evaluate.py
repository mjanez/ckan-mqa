# inbuilt libraries
import urllib.request
from pyshacl import validate
import rdflib
import logging

# custom functions
from config.log import get_log_module


# Info
WEIGHT_TOTAL = 405  
FINDABILITY = 'Findability'
ACCESIBILITY = 'Accessibility'
INTEROPERABILITY = 'Interoperability'
REUSABILITY = 'Reusability'
CONTEXTUALITY = 'Contextuality'
DISTRIBUTION = 'dcat:Distribution'
DATASET = 'dcat:Dataset'
CODE_200 = ' code=200'
FROM_VOCABULARY = ' from vocabulary'
TIMEOUT = 30
CKAN_URIS = 'ckan_uris'
CKAN = 'ckan'
EDP = 'edp'
NTI = 'nti'

log_module = get_log_module()

def make_request(url):
    request = urllib.request.Request(url)
    # Make the HTTP request.
    response = urllib.request.urlopen(request, timeout = TIMEOUT )
    assert 200 <= response.code < 400

def load_vocabulary(vocabulary_file, field = 0, app_dir = '/app'):
    vocabulary = []
    vocabulary_file_path =  f"{app_dir}/ckan2mqa/assets/{vocabulary_file}"
    with open(vocabulary_file_path) as fp:
        for line in fp:
            words = line.strip().split(',')
            if len(words) > field:
                if words[field] != '':
                    vocabulary.append(words[field])
    return vocabulary

def contains_vocabulary_word(vocabulary, word):
    for value in vocabulary:
        if value.lower().find(word.lower()) >= 0:
            # print (value, word)
            return True
    return False

def contains_word_vocabulary(vocabulary, word):
    for value in vocabulary:
        if word.lower().find(value.lower()) >= 0:
            return True
    return False


class MqaEvaluate:

    def __init__(self, catalog_rdf_file, catalog_rdf_filename, catalog_file_folder, shapes_turtle_file, shapes_vocabulary, shapes_deprecateduris, app_dir = "/app", catalog_format = 'application/rdf+xml', catalog_type = CKAN):
        self.app_dir = app_dir
        self.catalog = catalog_rdf_file
        self.catalog_filename = catalog_rdf_filename
        self.shapes = shapes_turtle_file
        self.shapes_vocabulary = shapes_vocabulary
        self.shapes_deprecateduris = shapes_deprecateduris
        self.graph = rdflib.Graph()
        self.graph.parse(source=self.catalog, format = catalog_format)
        self.datasetCount = self.count_entities(DATASET)
        self.distributionCount = self.count_entities(DISTRIBUTION)
        self.totalPoints = 0
        self.catalog_type = catalog_type
        self.catalog_file_folder = catalog_file_folder
        self.results_file = open(f"{self.catalog_file_folder}/{self.catalog_filename}_results.txt", 'w')

    def shacl(self):
        '''
        https://github.com/RDFLib/pySHACL
        More information about SHACL at https://www.w3.org/TR/shacl/
        Shapes files retrieved from https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/dcat-application-profile-data-portals-europe/releases
        The shacl service of EDP (https://www.europeandataportal.eu/shacl/) also has a copy of these files at https://gitlab.com/european-data-portal/metrics/edp-metrics-validating-shacl/-/tree/master/src/main/resources/rdf/shapes
        '''
        sg = rdflib.Graph()
        sg.parse(source=self.shapes, format='turtle')
        sg.parse(source=self.shapes_vocabulary, format='turtle')
        sg.parse(source=self.shapes_deprecateduris, format='turtle')

        try:
            r = validate(self.graph, shacl_graph=sg, inference='rdfs', abort_on_first=True)
            conforms, results_graph, results_text = r
            if not conforms:
                error_file_name = f"{self.catalog_file_folder}/{self.catalog_filename}_errors_SHACL.txt"
                with open(error_file_name, "w", encoding="utf-8") as text_file:
                    text_file.write(results_text)
            return conforms
        except Exception as err:
            logging.error(f"{log_module}:Exception occurred: {err}")
            return False

    def count_entities(self, entity):
        qres = self.graph.query("""
                   PREFIX dct:<http://purl.org/dc/terms/>
                   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                   PREFIX dcat: <http://www.w3.org/ns/dcat#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    SELECT  (count(DISTINCT ?resource) as ?values)  WHERE {
                        ?resource rdf:type """+ entity +""" .
                    }
                    """)
        for row in qres:
            count = int(row["values"])
        return count

    def count_entity_property(self, entity, property):
        qres = self.graph.query("""
                   PREFIX dct:<http://purl.org/dc/terms/>
                   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                   PREFIX dcat: <http://www.w3.org/ns/dcat#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    SELECT  (count(DISTINCT ?resource) as ?values)  WHERE {
                        ?resource rdf:type """+ entity + """ .
        	            ?resource """ + property +""" ?value .
                    }
                    """)
        for row in qres:
            count = int(row["values"])
        return count

    def count_uris_formats_from_vocabulary(self, vocabulary, entity = DISTRIBUTION, property = 'dct:format'):
        '''
        The format returned by EDP or CKAN GeoDCAT-AP instance is a URL, the last token of the URL is the label of the format, e.g. http://publications.europa.eu/resource/authority/file-type/XML
        '''
        qres = self.graph.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            SELECT ?value (COUNT(?value) as ?count)
            WHERE {
                ?resource a """ + entity + """ .
                ?resource """ + property + """ ?value .
            }
            GROUP BY ?value
            """)
        count = 0
        for row in qres:
            format = row["value"]
            words = format.strip().split('/')
            if len(words) > 0:
                format_label = words[len(words)-1]
                partialCount = int(row["count"])
                # print('Recognised format: ', format_label, partialCount)
                if contains_vocabulary_word(vocabulary,format_label):
                    count += partialCount
        return count

    def count_nti_formats_from_vocabulary(self, vocabulary):
        '''
        The format returned by NTI models is a dct:IMT
        '''
        qres = self.graph.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            SELECT ?value (COUNT(?value) as ?count)
            WHERE {
                ?resource a dcat:Distribution .
                ?resource dct:format ?format .
                ?format rdfs:label ?value .
            }
            GROUP BY ?value
            """)
        count = 0
        for row in qres:
            format = row["value"]
            words = format.strip().split('/')
            if len(words) > 0:
                format_label = words[len(words)-1]
                partialCount = int(row["count"])
                # print('Recognised format: ', format_label, partialCount)
                if contains_vocabulary_word(vocabulary,format_label):
                    count += partialCount
        return count

    def count_values_contained_in_vocabulary(self, entity, property, vocabulary):
        qres = self.graph.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            SELECT ?value (COUNT(?value) as ?count)
            WHERE {
                ?resource a """ + entity + """ .
                ?resource """ + property + """ ?value .
            }
            GROUP BY ?value
            """)
        count = 0
        for row in qres:
            format = row["value"]
            partialCount = int(row["count"])
            #if contains_exact(vocabulary,format):
            if contains_vocabulary_word(vocabulary, format):
                    count += partialCount
        return count

    def count_values_containing_vocabulary(self, entity, property, vocabulary):
        qres = self.graph.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            SELECT ?value (COUNT(?value) as ?count)
            WHERE {
                ?resource a """ + entity + """ .
                ?resource """ + property + """ ?value .
            }
            GROUP BY ?value
            """)
        count = 0
        for row in qres:
            value = row["value"]
            partialCount = int(row["count"])
            # print(value, partialCount)
            if contains_word_vocabulary(vocabulary, value):
                count += partialCount
        return count

    def count_urls_with_200_code(self, property):
        qres = self.graph.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            SELECT ?value (COUNT(?value) as ?count)
            WHERE {
                ?resource a dcat:Distribution .
                ?resource """+ property+""" ?value
            }
            GROUP BY ?value
            """)
        count = 0

        error_file_name = f"{self.catalog_file_folder}/{self.catalog_filename}_errors_{property.replace(':','_')}.txt"
        with open(error_file_name, "w", encoding="utf-8") as text_file:
            for row in qres:
                url = row["value"]
                partialCount = int(row["count"])
                try:
                    make_request(url)
                    count += partialCount
                except:
                    text_file.write(url + '\t' + str(partialCount) + '\n')
                    #print(url + " not reached")
        return count

    def print(self, dimension, property, count, population, weight):
        if population > 0:
            percentage = count / population
        else:
            percentage = 0
        if count > 0:
            partialPoints = round(percentage * weight, 2)
            self.totalPoints += partialPoints
        else:
            partialPoints = 0
        self.results_file.write(f"{dimension}\t{property}\t{count}\t{population}\t{round(percentage, 2)}\t{partialPoints}\t{weight}\n")

    def get_rating(self):
        if self.totalPoints >= 351:
            return "Excellent"
        elif self.totalPoints >= 221:
            return "Good"
        elif self.totalPoints >= 121:
            return "Sufficient"
        else:
            return "Bad"

    def findability_keywords_available(self):
        dimension = FINDABILITY
        entity = DATASET
        property = 'dcat:keyword'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 30)

    def findability_category_available(self):
        dimension = FINDABILITY
        entity = DATASET
        property = 'dcat:theme'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 30)

    def findability_spatial_available(self):
        dimension = FINDABILITY
        entity = DATASET
        property = 'dct:spatial'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 20)

    def findability_temporal_available(self):
        dimension = FINDABILITY
        entity = DATASET
        property = 'dct:temporal'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 20)

    def accesibility_accessURL_code_200(self):
        dimension = ACCESIBILITY
        entity = DISTRIBUTION
        property = 'dcat:accessURL'
        count = self.count_urls_with_200_code(property)
        population = self.distributionCount
        self.print(dimension, property + CODE_200, count, population, 50)

    def accesibility_downloadURL_available(self):
        dimension = ACCESIBILITY
        entity = DISTRIBUTION
        property = 'dcat:downloadURL'
        count = self.count_entity_property(entity, property)
        population = self.distributionCount
        self.print(dimension, property, count, population, 20)

    def accesibility_downloadURL_code_200(self):
        dimension = ACCESIBILITY
        entity = DISTRIBUTION
        property = 'dcat:downloadURL'
        count = self.count_urls_with_200_code(property)
        population = self.distributionCount
        self.print(dimension, property + CODE_200, count, population, 30)

    def interoperability_format_available(self):
        dimension = INTEROPERABILITY
        entity = DISTRIBUTION
        property = 'dct:format'
        count = self.count_entity_property(entity, property)
        population = self.distributionCount
        self.print(dimension, property, count, population, 20)

    def interoperability_mediaType_available(self):
        dimension = INTEROPERABILITY
        entity = DISTRIBUTION
        property = 'dcat:mediaType'
        count = self.count_entity_property(entity, property)
        population = self.distributionCount
        self.print(dimension, property, count, population, 10)

    def interoperability_format_from_vocabulary(self):
        '''
        https://www.iana.org/assignments/media-types/media-types.xhtml
        '''
        dimension = INTEROPERABILITY
        entity = DISTRIBUTION
        property = 'dct:format'
        vocabulary = load_vocabulary('/vocabs/media-types.csv', 0, self.app_dir)
        if self.catalog_type == CKAN_URIS or self.catalog_type == EDP:
                count = self.count_values_containing_vocabulary(entity,property,vocabulary)
        # Import vocabs label and count values
        elif self.catalog_type == CKAN:
            vocabulary = load_vocabulary('/vocabs/media-types.csv', 1, self.app_dir)
            count = self.count_values_contained_in_vocabulary(entity, property, vocabulary)
        else:
            #NTI
            count = self.count_nti_formats_from_vocabulary(vocabulary)
        population = self.distributionCount
        self.print(dimension, property + FROM_VOCABULARY, count, population, 10)

    def interoperability_format_mediatype_from_vocabulary(self):
        '''
        dct:format = http://publications.europa.eu/resource/authority/file-type
        dcat:mediaType = https://www.iana.org/assignments/media-types/media-types.xhtml
        '''
        dimension = INTEROPERABILITY
        entity = DISTRIBUTION
        properties = ['dct:format', 'dcat:mediaType']
        vocabulary_files = {
            'dct:format': '/vocabs/file-types.csv',
            'dcat:mediaType': '/vocabs/media-types.csv'
        }
        counts = []
        for property in properties:
            vocabulary = load_vocabulary(vocabulary_files[property], 0, self.app_dir)
            if self.catalog_type == CKAN_URIS or self.catalog_type == EDP:
                count = self.count_values_containing_vocabulary(entity, property, vocabulary)
            elif self.catalog_type == CKAN:
                vocabulary = load_vocabulary(vocabulary_files[property], 1, self.app_dir)
                count = self.count_values_contained_in_vocabulary(entity, property, vocabulary)
            else:
                count = self.count_nti_formats_from_vocabulary(vocabulary)
            counts.append(count)
        # population is distributionCount * number of properties
        population = self.distributionCount * len(properties)
        self.print(dimension, '/'.join(properties) + FROM_VOCABULARY, sum(counts), population, 10)

    def interoperability_format_nonProprietary(self):
        '''
        https://gitlab.com/european-data-portal/edp-vocabularies/-/blob/master/Custom%20Vocabularies/edp-non-proprietary-format.rdf
        '''
        dimension = INTEROPERABILITY
        entity = DISTRIBUTION
        property = 'dct:format'
        vocabulary = load_vocabulary('/vocabs/non-proprietary.csv', 0, self.app_dir)
        if self.catalog_type == CKAN_URIS or self.catalog_type == EDP:
                count = self.count_values_containing_vocabulary(entity,property,vocabulary)
        # Import vocabs label and count values
        elif self.catalog_type == CKAN:
            vocabulary = load_vocabulary('/vocabs/non-proprietary.csv', 1, self.app_dir)
            count = self.count_values_contained_in_vocabulary(entity, property, vocabulary)
        else:
            #NTI
            count = self.count_nti_formats_from_vocabulary(vocabulary)  
        population = self.distributionCount
        self.print(dimension, property + ' non-proprietary', count, population, 20)

    def interoperability_format_machineReadable(self):
        '''
        https://gitlab.com/european-data-portal/edp-vocabularies/-/blob/master/Custom%20Vocabularies/edp-machine-readable-format.rdf
        '''
        dimension = INTEROPERABILITY
        entity = DISTRIBUTION
        property = 'dct:format'
        vocabulary = load_vocabulary('/vocabs/machine-readable.csv', 0, self.app_dir)
        if self.catalog_type == CKAN_URIS or self.catalog_type == EDP:
                count = self.count_values_containing_vocabulary(entity,property,vocabulary)
        # Import vocabs label and count values
        elif self.catalog_type == CKAN:
            vocabulary = load_vocabulary('/vocabs/machine-readable.csv', 1, self.app_dir)
            count = self.count_values_contained_in_vocabulary(entity, property, vocabulary)
        else:
            #NTI
            count = self.count_nti_formats_from_vocabulary(vocabulary)
        population = self.distributionCount
        self.print(dimension, property + ' machine-readable', count, population, 20)

    def interoperability_DCAT_AP_compliance(self):
        dimension = INTEROPERABILITY
        entity = DATASET
        property = 'DCAT-AP compliance'
        if self.catalog is not None and self.shapes is not None:
            conforms = self.shacl()
            if conforms:
                count = self.datasetCount
            else:
                count = 0
        else:
            count = -1
        population = self.datasetCount
        self.print(dimension, property, count, population, 30)

    def reusability_license_available(self):
        dimension = REUSABILITY
        entity = DISTRIBUTION
        property = 'dct:license'
        count = self.count_entity_property(entity, property)
        population = self.distributionCount
        self.print(dimension, property, count, population, 20)

    def reusability_license_from_vocabulary(self):
        '''
        https://gitlab.com/european-data-portal/edp-vocabularies/-/blob/master/Custom%20Vocabularies/edp-licences-skos.rdf
        '''
        dimension = REUSABILITY
        entity = DISTRIBUTION
        property = 'dct:license'
        vocabulary = load_vocabulary('/vocabs/licenses.csv', 0, self.app_dir)
        count = self.count_values_containing_vocabulary(entity,property,vocabulary)
        population = self.distributionCount
        self.print(dimension, property + FROM_VOCABULARY, count, population, 10)

    def reusability_accessRights_available(self):
        dimension = REUSABILITY
        entity = DATASET
        property = 'dct:accessRights'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 10)

    def reusability_accessRights_from_vocabulary(self):
        '''
        https://gitlab.com/european-data-portal/edp-vocabularies/-/blob/master/EU%20Vocabularies/access-right-skos.rdf
        '''
        dimension = REUSABILITY
        entity = DATASET
        property = 'dct:accessRights'
        vocabulary = load_vocabulary('/vocabs/access-right.csv', 0, self.app_dir)
        count = self.count_values_contained_in_vocabulary(entity,property,vocabulary)
        population = self.datasetCount
        self.print(dimension, property + FROM_VOCABULARY, count, population, 5)

    def reusability_contactPoint_available(self):
        dimension = REUSABILITY
        entity = DATASET
        property = 'dcat:contactPoint'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 20)

    def reusability_publisher_available(self):
        dimension = REUSABILITY
        entity = DATASET
        property = 'dct:publisher'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 10)

    def contextuality_rights_available(self):
        dimension = CONTEXTUALITY
        entity = DISTRIBUTION
        property = 'dct:rights'
        count = self.count_entity_property(entity, property)
        population = self.distributionCount
        self.print(dimension, property, count, population, 5)

    def contextuality_fileSize_available(self):
        dimension = CONTEXTUALITY
        entity = DISTRIBUTION
        property = 'dcat:byteSize'
        count = self.count_entity_property(entity, property)
        population = self.distributionCount
        self.print(dimension, property, count, population, 5)

    def contextuality_issued_available(self):
        dimension = CONTEXTUALITY
        entity = DATASET
        property = 'dct:issued'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 5)

    def contextuality_modified_available(self):
        dimension = CONTEXTUALITY
        entity = DATASET
        property = 'dct:modified'
        count = self.count_entity_property(entity, property)
        population = self.datasetCount
        self.print(dimension, property, count, population, 5)

    def evaluate(self):
        self.results_file.write(f"Dimension\tIndicator/property\tCount\tPopulation\tPercentage\tPoints\tWeight\n")
        self.findability_keywords_available()
        self.findability_category_available()
        self.findability_spatial_available()
        self.findability_temporal_available()
        self.accesibility_accessURL_code_200()
        self.accesibility_downloadURL_available()
        self.accesibility_downloadURL_code_200()
        self.interoperability_format_available()
        self.interoperability_mediaType_available()
        self.interoperability_format_mediatype_from_vocabulary()
        self.interoperability_format_nonProprietary()
        self.interoperability_format_machineReadable()
        self.interoperability_DCAT_AP_compliance()
        self.reusability_license_available()
        self.reusability_license_from_vocabulary()
        self.reusability_accessRights_available()
        self.reusability_accessRights_from_vocabulary()
        self.reusability_contactPoint_available()
        self.reusability_publisher_available()
        self.contextuality_rights_available()
        self.contextuality_fileSize_available()
        self.contextuality_issued_available()
        self.contextuality_modified_available()
        
        self.results_file.write(f"Total points\tRating: {self.get_rating()}\t\t\t{round(self.totalPoints/WEIGHT_TOTAL, 2)}\t{round(self.totalPoints, 2)}\t{WEIGHT_TOTAL}\n")
        self.results_file.close()
        logging.info(f"{log_module}:{self.catalog_filename} total points: {round(self.totalPoints, 2)}/{WEIGHT_TOTAL}")


