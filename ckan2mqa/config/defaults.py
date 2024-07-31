import os
from pathlib import Path
from urllib.parse import urljoin

from rdflib import Namespace


EU_VOCABULARIES = [
    {
        'name': 'Access Right',
        'base_filename': 'access-right',
        'url': 'http://publications.europa.eu/resource/authority/access-right',
        'description': 'Access rights, CSV fields: URI, Label'
    },
    {
        'name': 'File Types',
        'base_filename': 'file-types',
        'url': 'http://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/file-type/rdf/skos_ap_act/filetypes-skos-ap-act.rdf&fileName=filetypes-skos-ap-act.rdf',
        'description': 'File Types, CSV fields: URI, Label, Non-Proprietary format (true/false)'
    },
    {
        'name': 'IANA Media Types',
        'base_filename': 'media-types',
        'url': 'http://www.iana.org/assignments/media-types/media-types.xml',
        'description': 'File Types, CSV fields: URI, Label'
    },
    {
        'name': 'Licenses',
        'base_filename': 'licenses',
        'url': 'http://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http://publications.europa.eu/resource/distribution/licence/rdf/skos_ap_act/licences-skos-ap-act.rdf&fileName=licences-skos-ap-act.rdf',
        'description': 'Licenses, CSV fields: URI, Label, EUVocab URI'
    }
    # Add more URLs and their respective configurations here as needed
]

# Namespaces
EUROVOC = Namespace('http://publications.europa.eu/ontology/euvoc#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
DC = Namespace('http://purl.org/dc/elements/1.1/')
HYDRA = 'http://www.w3.org/ns/hydra/core#'

# Directories
APP_DIR = os.environ.get('APP_DIR', '/app')
VOCABS_DIR = Path(APP_DIR) / 'ckan2mqa/assets/vocabs'

# Evaluation vars
EVALUATION_DEFAULT_FORMAT = 'catalog.ttl'
CKAN_API_OUTPUT = 'local_evaluation'
CKAN_API_CKAN_URL = 'http://localhost:5000'
# evaluation_edp_search
EDP_API_OUTPUT = 'edp'
EDP_API_CKAN_BASE_URL = 'https://www.europeandataportal.eu'
EDP_API_CKAN_URL = urljoin(EDP_API_CKAN_BASE_URL, 'data/search')
## evaluation_sparql
EDP_SPARQL_OUTPUT = EDP_API_OUTPUT + '/'
EDP_SPARQL_URL = urljoin(EDP_API_CKAN_BASE_URL, 'sparql')
EDP_SPARQL_EVALUATION_PUBLISHER = os.environ.get('EDP_SPARQL_EVALUATION_', 'http://datos.gob.es/recurso/sector-publico/org/Organismo/E00003801')
EDP_SPARQL_EVALUATION_KEYWORD = os.environ.get('EDP_SPARQL_EVALUATION_KEYWORD', 'environment')

# HTTP parameters
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# MQA Evaluation. Vars
FINDABILITY = 'Findability'
ACCESIBILITY = 'Accessibility'
INTEROPERABILITY = 'Interoperability'
REUSABILITY = 'Reusability'
CONTEXTUALITY = 'Contextuality'
DISTRIBUTION = 'dcat:Distribution'
DATASET = 'dcat:Dataset'
CODE_200 = ' code=200'
FROM_VOCABULARY = ' from vocabulary'
TIMEOUT = 10
CKAN_URIS = 'ckan_uris'
CKAN = 'ckan'
EDP = 'edp'
NTI = 'nti'


# MQA Evaluation. Rating
MQA_RATING_THRESHOLDS = {
    "Excellent": 351,
    "Good": 221,
    "Sufficient": 121,
    "Bad": 0,
    "WEIGHT_TOTAL": 405
}
WEIGHT_TOTAL = MQA_RATING_THRESHOLDS["WEIGHT_TOTAL"]

# MQA Evaluation. Indicators
MQA_INDICATORS = {
    'findability_keywords_available': {
        'dimension': FINDABILITY,
        'entity': DATASET,
        'property': 'dcat:keyword',
        'population_attr': 'datasetCount',
        'points': 30,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating findability keywords availability.",
        'function': 'findability_keywords_available'
    },
    'findability_category_available': {
        'dimension': FINDABILITY,
        'entity': DATASET,
        'property': 'dcat:theme',
        'population_attr': 'datasetCount',
        'points': 30,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating findability category availability.",
        'function': 'findability_category_available'
    },
    'findability_spatial_available': {
        'dimension': FINDABILITY,
        'entity': DATASET,
        'property': 'dct:spatial',
        'population_attr': 'datasetCount',
        'points': 20,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating findability spatial availability.",
        'function': 'findability_spatial_available'
    },
    'findability_temporal_available': {
        'dimension': FINDABILITY,
        'entity': DATASET,
        'property': 'dct:temporal',
        'population_attr': 'datasetCount',
        'points': 20,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating findability temporal availability.",
        'function': 'findability_temporal_available'
    },
    'accesibility_accessURL_code_200': {
        'dimension': ACCESIBILITY,
        'entity': DISTRIBUTION,
        'property': 'dcat:accessURL',
        'population_attr': 'distributionCount',
        'points': 50,
        'count_method': 'count_urls_with_200_code',
        'property_suffix': CODE_200,
        'log_message': "Evaluating accessibility access URL code 200.",
        'function': 'accesibility_accessURL_code_200'
    },
    'accesibility_downloadURL_available': {
        'dimension': ACCESIBILITY,
        'entity': DISTRIBUTION,
        'property': 'dcat:downloadURL',
        'population_attr': 'distributionCount',
        'points': 20,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating accessibility download URL availability.",
        'function': 'accesibility_downloadURL_available'
    },
    'accesibility_downloadURL_code_200': {
        'dimension': ACCESIBILITY,
        'entity': DISTRIBUTION,
        'property': 'dcat:downloadURL',
        'population_attr': 'distributionCount',
        'points': 30,
        'count_method': 'count_urls_with_200_code',
        'property_suffix': CODE_200,
        'log_message': "Evaluating accessibility download URL code 200.",
        'function': 'accesibility_downloadURL_code_200'
    },
    'interoperability_format_available': {
        'dimension': INTEROPERABILITY,
        'entity': DISTRIBUTION,
        'property': 'dct:format',
        'population_attr': 'distributionCount',
        'points': 20,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating interoperability format availability.",
        'function': 'interoperability_format_available'
    }, 
    'interoperability_mediaType_available':{
        'dimension': INTEROPERABILITY,
        'entity': DISTRIBUTION,
        'property': 'dcat:mediaType',
        'population_attr': 'distributionCount',
        'points': 10,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating interoperability media type availability.",
        'function': 'interoperability_mediaType_available'
    },
    'interoperability_format_from_vocabulary': {
        'dimension': INTEROPERABILITY,
        'entity': DISTRIBUTION,
        'property': 'dct:format',
        'population_attr': 'distributionCount',
        'points': 10,
        'count_method': 'count_values_containing_vocabulary',
        'log_message': "Evaluating interoperability format from vocabulary.",
        'function': 'interoperability_format_from_vocabulary'
    },
    'interoperability_format_mediatype_from_vocabulary': {
        'dimension': INTEROPERABILITY,
        'entity': DISTRIBUTION,
        'property': ['dct:format', 'dcat:mediaType'],
        'population_attr': 'distributionCount',
        'points': 10,
        'count_method': 'count_values_containing_vocabulary',
        'log_message': "Evaluating interoperability format and media type from vocabulary.",
        'function': 'interoperability_format_mediatype_from_vocabulary'
    },
    'interoperability_format_nonProprietary': {
        'dimension': INTEROPERABILITY,
        'entity': DISTRIBUTION,
        'property': 'dct:format',
        'population_attr': 'distributionCount',
        'points': 20,
        'count_method': 'count_values_containing_vocabulary',
        'log_message': "Evaluating interoperability non-proprietary format.",
        'function': 'interoperability_format_nonProprietary'
    },
    'interoperability_format_machineReadable': {
        'dimension': INTEROPERABILITY,
        'entity': DISTRIBUTION,
        'property': 'dct:format',
        'population_attr': 'distributionCount',
        'points': 20,
        'count_method': 'count_values_containing_vocabulary',
        'log_message': "Evaluating interoperability machine-readable format.",
        'function': 'interoperability_format_machineReadable'
    },
    'interoperability_DCAT_AP_compliance': {
        'dimension': INTEROPERABILITY,
        'entity': DATASET,
        'property': 'DCAT-AP compliance',
        'population_attr': 'datasetCount',
        'points': 30,
        'count_method': 'shacl',
        'log_message': "Evaluating interoperability DCAT-AP compliance.",
        'function': 'interoperability_DCAT_AP_compliance'
    },
    'reusability_license_available': {
        'dimension': REUSABILITY,
        'entity': DATASET,
        'property': 'dcat:license',
        'population_attr': 'distributionCount',
        'points': 20,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating reusability license availability.",
        'function': 'reusability_license_available'
    },
    'reusability_license_from_vocabulary': {
        'dimension': REUSABILITY,
        'entity': DISTRIBUTION,
        'property': 'dct:license',
        'population_attr': 'distributionCount',
        'points': 10,
        'count_method': 'count_values_containing_vocabulary',
        'log_message': "Evaluating reusability license from vocabulary.",
        'function': 'reusability_license_from_vocabulary'
    },    
    'reusability_accessRights_available': {
        'dimension': REUSABILITY,
        'entity': DATASET,
        'property': 'dcat:accessRights',
        'population_attr': 'datasetCount',
        'points': 10,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating reusability access rights availability.",
        'function': 'reusability_accessRights_available'
    },
    'reusability_accessRights_from_vocabulary': {
        'dimension': REUSABILITY,
        'entity': DATASET,
        'property': 'dct:accessRights',
        'population_attr': 'datasetCount',
        'points': 5,
        'count_method': 'count_values_contained_in_vocabulary',
        'log_message': "Evaluating reusability access rights from vocabulary.",
        'function': 'reusability_accessRights_from_vocabulary'
    },
    'reusability_contactPoint_available': {
        'dimension': REUSABILITY,
        'entity': DATASET,
        'property': 'dcat:contactPoint',
        'population_attr': 'datasetCount',
        'points': 20,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating reusability contact point availability.",
        'function': 'reusability_contactPoint_available'
    },
    'reusability_publisher_available': {
        'dimension': REUSABILITY,
        'entity': DATASET,
        'property': 'dct:publisher',
        'population_attr': 'datasetCount',
        'points': 10,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating reusability publisher availability.",
        'function': 'reusability_publisher_available'
    },
    'contextuality_rights_available': {
        'dimension': CONTEXTUALITY,
        'entity': DISTRIBUTION,
        'property': 'dct:rights',
        'population_attr': 'distributionCount',
        'points': 5,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating contextuality rights availability.",
        'function': 'contextuality_rights_available'
    },
    'contextuality_fileSize_available': {
        'dimension': CONTEXTUALITY,
        'entity': DISTRIBUTION,
        'property': 'dcat:byteSize',
        'population_attr': 'distributionCount',
        'points': 5,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating contextuality file size availability.",
        'function': 'contextuality_fileSize_available'
    },
    'contextuality_issued_available': {
        'dimension': CONTEXTUALITY,
        'entity': DATASET,
        'property': 'dct:issued',
        'population_attr': 'datasetCount',
        'points': 5,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating contextuality issued date availability.",
        'function': 'contextuality_issued_available'
    },
    'contextuality_modified_available': {
        'dimension': CONTEXTUALITY,
        'entity': DATASET,
        'property': 'dct:modified',
        'population_attr': 'datasetCount',
        'points': 5,
        'count_method': 'count_entity_property',
        'log_message': "Evaluating contextuality modified date availability.",
        'function': 'contextuality_modified_available'
    }
}