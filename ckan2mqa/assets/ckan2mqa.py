from controller.mqa_evaluate import mqa_evaluate
from controller.rdf_management import download_rdf
import os
import ssl
import sys
import logging
from config.log import log_file


# Ennvars
TZ = os.environ.get('TZ', 'TZ')
CKAN_CATALOG_URL = os.environ.get('CKAN_CATALOG_URL', 'http://localhost:5000/catalog.rdf')
DEV_MODE = None
APP_DIR = os.environ.get('APP_DIR', '/app')
MQA_LOG_DIR = os.path.join(APP_DIR, 'log/mqa')
if not os.path.exists(MQA_LOG_DIR):
    os.makedirs(MQA_LOG_DIR)
VERSION = os.environ.get("VERSION", "0.1")
CATALOG_FILENAME = os.environ.get('CATALOG_FILE', 'catalog')
CATALOG_FILE = f"{APP_DIR}/log/mqa/{CATALOG_FILENAME}.rdf"
CATALOG_FORMAT = "application/rdf+xml"
DCATAP_FILES_VERSION = os.environ.get('DCATAP_FILES_VERSION', '2.1.1')
## DCAT-AP Files
SHAPESFILE = f"ckan2mqa/assets/{DCATAP_FILES_VERSION}/dcat-ap_{DCATAP_FILES_VERSION}_shacl_shapes.ttl"
SHAPESVOCABULARYFILE = f"ckan2mqa/assets/{DCATAP_FILES_VERSION}/dcat-ap_{DCATAP_FILES_VERSION}_shacl_mdr-vocabularies.shape.ttl"
SHAPESDEPRECATEDURISFILE = f"ckan2mqa/assets/{DCATAP_FILES_VERSION}/dcat-ap_{DCATAP_FILES_VERSION}_shacl_deprecateduris.ttl"
CKAN_METADATA_TYPE = os.environ.get('CKAN_METADATA_TYPE', 'ckan_uris')
log_module = "[ckan2mqa]"

def main():
    log_file(APP_DIR + "/log")
    logging.info(f"{log_module}:Version: {VERSION}")
    
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    url = CKAN_CATALOG_URL
    
    download_rdf(url, CATALOG_FILE)

    mqa_evaluate = mqa_evaluate(CATALOG_FILE, CATALOG_FILENAME, SHAPESFILE, SHAPESVOCABULARYFILE, SHAPESDEPRECATEDURISFILE, APP_DIR, CATALOG_FORMAT, CKAN_METADATA_TYPE)
    mqa_evaluate.evaluate() 

if __name__ == "__main__":
    if DEV_MODE == True or DEV_MODE == "True":
        # Allow other computers to attach to ptvsd at this IP address and port.
        ptvsd.enable_attach(address=("0.0.0.0", 5678), redirect_output=True)

        # Pause the program until a remote debugger is attached
        ptvsd.wait_for_attach()
    else:
        main()