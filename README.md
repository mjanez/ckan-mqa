<h1 align="center">Docker Metadata Quality Assessment (MQA) for CKAN/EDP catalogs</h1>
<p align="center">
<a href="https://github.com/mjanez/ckan-mqa"><img src="https://img.shields.io/badge/%20ckan-mqa-brightgreen" alt="mqa2ckan version"></a><a href="https://opensource.org/licenses/MIT"> <img src="https://img.shields.io/badge/license-Unlicense-brightgreen" alt="License: Unlicense"></a> <a href="https://github.com/mjanez/ckan-mqa/actions/workflows/docker/badge.svg" alt="License: Unlicense"></a>


<p align="center">
    <a href="#overview">Overview</a> •
    <a href="#quick-start">Quick start</a> •
    <a href="#debug">Debug</a> •
    <a href="#containers">Containers</a>
</p>

**Requirements**:
* [Docker](https://docs.docker.com/get-docker/)

## Overview
`ckan-mqa` offers a Docker Compose solution for performing [Metadata Quality Assessment (MQA)](https://data.europa.eu/mqa/methodology) on both CKAN endpoints and the European Data Portal catalogs. MQA is a crucial process to ensure the accuracy, completeness, and reliability of metadata, enhancing the overall data interoperability and accessibility.

This Docker Compose configuration integrates the powerful MQA toolset seamlessly with CKAN endpoints and European Data Portal catalogs, enabling users to perform in-depth assessments of metadata quality effortlessly. The setup provides an efficient way to run comprehensive quality checks on various metadata attributes, including data relevance, schema compliance, data format consistency, and adherence to standard vocabularies.

![5 MQA_dimensions png](https://github.com/mjanez/ckan-mqa/assets/96422458/0c54d8c3-e454-4a6a-bcd6-ebc0a0dae080)


>**Note**<br>
> It can be tested with an open data portal of the CKAN type such as: [mjanez/ckan-docker](https://github.com/mjanez/ckan-docker)[^1]

## Quick start
First copy the `.env.example` template as `.env` and configure by changing the `CKAN_CATALOG_URL`,  as well as the DCAT-AP Profile version (`DCATAP_FILES_VERSION`), if needed.

```bash
cp .env.example .env
```

Custom ennvars:
- `CKAN_CATALOG_URL`: URL of the CKAN catalog to be downloaded (i.e. `http://localhost:5000/catalog.rdf?q=organization:test`).
- `APP_DIR`: Path to the application folder in Docker.
- `TZ`: Timezone.
- `DCATAP_FILES_VERSION`: DCAT-AP version (Avalaibles: 2.0.1, 2.1.0, 2.1.1).
- `UPDATE_VOCABS`: Update vocabs from the EU Publications Office at start (`True` or `False`).
- `CKAN_METADATA_TYPE`: CKAN Metadata elements type: `ckan_uris` for GeoDCAT-AP schema with all elements described by URIs (e.g. `dct:format` = <http://publications.europa.eu/resource/authority/file-type/XML>) or `ckan` if used a CKAN default schema with label metadata elements (e.g. `dct:format` = "XML").

### With docker compose
To deploy the environment, `docker compose` will build the latest image ([`ghcr.io/mjanez/ckan-mqa:latest`](https://github.com/mjanez/ckan-mqa/pkgs/container/ckan-mqa)).

```bash
git clone https://github.com/mjanez/ckan-mqa
cd ckan-mqa

docker compose up --build

# Or detached mode
docker compose up -d --build
```

>**Note**:<br>
> Deploy the dev (local build) `docker-compose.dev.yml` with:
>
>```bash
> docker compose -f docker-compose.dev.yml up --build
>```


>**Note**:<br>
>If needed, to build a specific container simply run:
>
>```bash
>  docker build -t target_name xxxx/
>```

### Without Docker
Dependencies:
```bash
python3 -m pip install --user pip3
pip3 install pdm
pdm install --no-self
```

Run:
```bash
pdm run python ckan2mqa/ckan2mqa.py
```

## Debug
### VSCode
1. Build and run container.
2. Attach Visual Studio Code to container
3. Start debugging on `ckan2mqa.py` Python file (`Debug the currently active Python file`).

## Containers
List of *containers*:
### Base images
| Repository | Type | Docker tag | Size | Notes |
| --- | --- | --- | --- | --- |
| python 3.11| base image | `python/python:3.11-slim` | 45.57 MB |  - |

### Built images
| Repository | Type | Docker tag | Size | Notes |
| --- | --- | --- | --- | --- |
| mjanez/ckan-mqa| custom image | `mjanez/ckan-mqa:v*.*.*` | 264 MB |  Tag version. |
| mjanez/ckan-mqa| custom image | `mjanez/ckan-mqa:latest` | 264 MB |  Latest stable version. |
| mjanez/ckan-mqa| custom image | `mjanez/ckan-mqa:main` | 264 MB |  Dev version.  |


[^1]: A custom installation of Docker Compose with specific extensions for spatial data and [GeoDCAT-AP](https://github.com/SEMICeu/GeoDCAT-AP)/[INSPIRE](https://github.com/INSPIRE-MIF/technical-guidelines) metadata [profiles](https://en.wikipedia.org/wiki/Geospatial_metadata).
