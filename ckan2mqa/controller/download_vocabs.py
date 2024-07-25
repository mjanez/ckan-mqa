# inbuilt libraries
import csv
import requests
from datetime import datetime
from pathlib import Path
import os
import logging

# custom functions
from config.log import get_log_module

# third-party libraries
from rdflib import Graph, Namespace, RDF
from xml.etree import ElementTree as ET


log_module = get_log_module()

RDF_DATA = [
    {
        "name": "Access Right",
        "base_filename": "access-right",
        "url": "http://publications.europa.eu/resource/authority/access-right",
        "description": "Access rights, CSV fields: URI, Label"
    },
    {
        "name": "File Types",
        "base_filename": "file-types",
        "url": "http://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http%3A%2F%2Fpublications.europa.eu%2Fresource%2Fcellar%2F0e8c3dc2-103f-11ee-b12e-01aa75ed71a1.0001.03%2FDOC_1&fileName=filetypes-skos-ap-act.rdf",
        "description": "File Types, CSV fields: URI, Label, Non-Proprietary format (true/false)"
    },
    {
        "name": "IANA Media Types",
        "base_filename": "media-types",
        "url": "http://www.iana.org/assignments/media-types/media-types.xml",
        "description": "File Types, CSV fields: URI, Label"
    },
    {
        "name": "Licenses",
        "base_filename": "licenses",
        "url": "https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http%3A%2F%2Fpublications.europa.eu%2Fresource%2Fdistribution%2Flicence%2F20230927-0%2Frdf%2Fskos_ap_act%2Flicences-skos-ap-act.rdf&fileName=licences-skos-ap-act.rdf",
        "description": "Licenses, CSV fields: URI, Label, EUVocab URI"
    }
    # Add more URLs and their respective configurations here as needed
]
EUROVOC = Namespace("http://publications.europa.eu/ontology/euvoc#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
APP_DIR = os.environ.get('APP_DIR', '/app')
VOCABS_DIR = Path(APP_DIR) / "ckan2mqa/assets/vocabs"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

class RdfFile:
    def __init__(self, base_filename, url, description, name):
        self.base_filename = base_filename
        self.url = url
        self.description = description
        self.name = name

    def extract_description(self, rdf_content, rdf_url):
        raise NotImplementedError


class BasicRdfFile(RdfFile):
    def extract_description(self, rdf_content, rdf_url):
        graph = Graph().parse(data=rdf_content, format='xml')
        data = set()

        for concept in graph.subjects():
            uri = str(concept)
            label = concept.split('/')[-1]
            if uri != rdf_url and label != rdf_url.split('/')[-1]:
                data.add((uri, label))

        return data

class LicenseRdfFile(RdfFile):
    def extract_description(self, rdf_content, rdf_url):
        graph = Graph().parse(data=rdf_content, format='xml')
        data = set()

        for concept in graph.subjects(RDF.type, SKOS.Concept):
            label = concept.split('/')[-1]
            eu_uri = concept
            uri = str(graph.value(concept, SKOS.exactMatch, default=eu_uri))
            if concept != rdf_url and label != rdf_url.split('/')[-1]:
                data.add((uri, label, eu_uri))

        return data

class FileTypesRdfFile(RdfFile):
    def extract_description(self, rdf_content, rdf_url):
        graph = Graph().parse(data=rdf_content, format='xml')
        data = set()
        non_proprietary_data = set()
        machine_readable_data = set()

        for concept in graph.subjects(RDF.type, EUROVOC.FileType):
            uri = str(concept)
            label = uri.split('/')[-1]
            non_prop_ext = str(graph.value(concept, EUROVOC.nonPropExt, default="false"))

            if uri != rdf_url and label != rdf_url.split('/')[-1]:
                data.add((uri, label, non_prop_ext))
                machine_readable_data.add((uri, label))
                if non_prop_ext == "true":
                    non_proprietary_data.add((uri, label))

        # Save non-proprietary data to separate CSV
        non_proprietary_file_name = f"non-propietary.csv"
        save_to_csv(non_proprietary_data, VOCABS_DIR / non_proprietary_file_name)
        logging.info(f"{log_module}:Non-proprietary data extracted and saved to {non_proprietary_file_name}")

        machine_readable_file_name = f"machine-readable.csv"
        save_to_csv(machine_readable_data, VOCABS_DIR / machine_readable_file_name)
        logging.info(f"{log_module}:Machine-readable data extracted and saved to {machine_readable_file_name}")

        return data

class MediaTypesRdfFile(RdfFile):
    def extract_description(self, xml_content, rdf_url):
        data = set()

        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()

        for record in root.findall(".//{http://www.iana.org/assignments}record"):
            name_elem = record.find("{http://www.iana.org/assignments}file")
            name = name_elem.text if name_elem is not None else ""
            label_elem = record.find("{http://www.iana.org/assignments}file")
            label = label_elem.text if label_elem is not None else ""

            if name != rdf_url.split('/')[-1]:
                uri = f"http://www.iana.org/assignments/media-types/{name}"
                data.add((uri, label))

        return data

def save_to_csv(data, csv_file):
    # Remove any None elements from the data list
    data = [d for d in data if d is not None]
    sorted_data = sorted(data, key=lambda x: x[1])  # Sort by label (2nd column)
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sorted_data)

def main():
    rdf_files = []
    for rdf_data in RDF_DATA:
        rdf_type = rdf_data["base_filename"]
        url = rdf_data["url"]
        description = rdf_data["description"]
        name = rdf_data["name"]

        if rdf_type == "access-right":
            rdf_files.append(BasicRdfFile(rdf_type, url, description, name))
        elif rdf_type == "licenses":
            rdf_files.append(LicenseRdfFile(rdf_type, url, description, name))
        elif rdf_type == "file-types":
            rdf_files.append(FileTypesRdfFile(rdf_type, url, description, name))
        elif rdf_type == "media-types":
            rdf_files.append(MediaTypesRdfFile(rdf_type, url, description, name))
        else:
            logging.warning(f"{log_module}:Unrecognized RDF type '{rdf_type}'. Skipping.")

    for rdf_file in rdf_files:
        try:
            response = requests.get(rdf_file.url, headers=headers, timeout=10)
            if response.status_code == 200:
                rdf_content = response.text
                extracted_data = rdf_file.extract_description(rdf_content, rdf_file.url)
                if extracted_data:  # Avoid creating CSV if no valid descriptions
                    file_name = f"{rdf_file.base_filename}.csv"
                    save_to_csv(extracted_data, VOCABS_DIR / file_name)
                    logging.info(f"{log_module}:{rdf_file.name} data extracted and saved to {file_name}")
            else:
                logging.warning(f"{log_module}:Failed to retrieve data for URL: {rdf_file.url}. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"{log_module}:An error occurred for URL: {rdf_file.url}. Error: {e}")

if __name__ == "__main__":
    main()