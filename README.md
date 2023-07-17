<h1 align="center">CKAN Docker Metadata Quality Assesment (MQA)</h1>
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
Docker compose environment for development and testing with CKAN Open Data portals.

>**Note**<br>
> In the integration with: [mjanez/ckan-docker](https://github.com/mjanez/ckan-docker)[^1], it is possible to test it with a CKAN-type open data portal.

## Quick start
First the `.env.example` template and configure by changing the `.env` file. Change `CKAN_CATALOG_URL`,  as well as the DCAT-AP Profile version (`DCATAP_FILES_VERSION`), if needed.

```bash
cp .env.example .env
```

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
| python 3.11| base image | `python/python:3.11-slim-bullseye` | 45.57 MB |  - |

### Built images
| Repository | Type | Docker tag | Size | Notes |
| --- | --- | --- | --- | --- |
| mjanez/ckan-mqa| custom image | `mjanez/ckan-mqa:v*.*.*` | 209 MB |  Tag version. |
| mjanez/ckan-mqa| custom image | `mjanez/ckan-mqa:latest` | 209 MB |  Latest stable version. |
| mjanez/ckan-mqa| custom image | `mjanez/ckan-mqa:main` | 209 MB |  Dev version.  |


[^1]: A custom installation of Docker Compose with specific extensions for spatial data and [GeoDCAT-AP](https://github.com/SEMICeu/GeoDCAT-AP)/[INSPIRE](https://github.com/INSPIRE-MIF/technical-guidelines) metadata [profiles](https://en.wikipedia.org/wiki/Geospatial_metadata).