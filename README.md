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

This Docker Compose configuration enhances a Python MQA software [^1] to integrates the powerful MQA toolset seamlessly with CKAN endpoints and European Data Portal catalogs, enabling users to perform in-depth assessments of metadata quality effortlessly. The setup provides an efficient way to run comprehensive quality checks on various metadata attributes, including data relevance, schema compliance, data format consistency, and adherence to standard vocabularies.

>**Note**<br>
> It can be tested with an open data portal of the CKAN type such as: [mjanez/ckan-docker](https://github.com/mjanez/ckan-docker)[^2]

### [Metadata Quality Assessment Methodology](https://data.europa.eu/mqa/methodology)
The MQA measures the quality of various indicators, each indicator is explained in the tables below. The results of the checks are stored as Data Quality Vocabulary ([DQV](https://www.w3.org/TR/vocab-dqv/)) . DQV is a specification of the W3C that is used to describe the quality of a dataset.

 **Dimension**    | **Maximal points** 
:----------------:|:------------------:
 Findability      | 100                
 Accessibility    | 100                
 Interoperability | 110                
 Reusability      | 75                 
 Contextuality    | 20                 
 *Sum*              | 405    

The dimensions are derived from the FAIR principles:
* **Findability**
The following table describes the metrics that help people and machines in finding datasets. A maximum of 100 points can be scored in this area.

* **Accessibility**
The following table describes which metrics are used to determine whether access to the data referenced by the distributions is guaranteed. A maximum of 100 points can be scored in this area.

* **Interoperability**
The following table describes the metrics used to determine whether a distribution is considered interoperable. According to the assumption 'identical content with several distributions', only the distribution with the highest number of points is used to calculate the points. A maximum of 110 points can be scored in this area

* **Reusability**
The following table describes which metrics are used to check the reusability of the data. A maximum of 75 points can be scored in this area.

* **Contextuality**
The following table show some light weight properties, that provide more context to the user. A maximum of 20 points can be scored in this area.

![5 MQA_dimensions png](https://github.com/mjanez/ckan-mqa/assets/96422458/0c54d8c3-e454-4a6a-bcd6-ebc0a0dae080)

The final rating happens via four rating groups. The mapping of the points to the rating category is shown in the table below. The representation of the rating in the MQA is expressed exclusively via the rating categories. This enables providers to achieve the highest rating even with a slight deduction of points.

 **Rating** | **Range of points** 
:----------:|:-------------------:
 Excellent  | 351 - 405           
 Good       | 221 – 350           
 Sufficient | 121 – 220           
 Bad        | 0 - 120             


#### Example of ckan-mqa results summary 

 **Dimension**    | **Indicator/property**                    | **Count** | **Population** | **Percentage** | **Points** | **Weight** 
:----------------:|:-----------------------------------------:|:---------:|:--------------:|:--------------:|:----------:|:----------:
 Findability      | dcat:keyword                              | 46        | 46             | 1.0            | 30.0       | 30         
 Findability      | dcat:theme                                | 46        | 46             | 1.0            | 30.0       | 30         
 Findability      | dct:spatial                               | 42        | 46             | 0.91           | 18.26      | 20         
 Findability      | dct:temporal                              | 0         | 46             | 0.0            | 0          | 20         
 Accessibility    | dcat:accessURL code=200                   | 255       | 255            | 1.0            | 50.0       | 50         
 Accessibility    | dcat:downloadURL                          | 0         | 255            | 0.0            | 0          | 20         
 Accessibility    | dcat:downloadURL code=200                 | 0         | 255            | 0.0            | 0          | 30         
 Interoperability | dct:format                                | 255       | 255            | 1.0            | 20.0       | 20         
 Interoperability | dcat:mediaType                            | 255       | 255            | 1.0            | 10.0       | 10         
 Interoperability | dct:format/dcat:mediaType from vocabulary | 378       | 510            | 0.74           | 7.41       | 10         
 Interoperability | dct:format non-proprietary                | 131       | 255            | 0.51           | 10.27      | 20         
 Interoperability | dct:format machine-readable               | 252       | 255            | 0.99           | 19.76      | 20         
 Interoperability | DCAT-AP compliance                        | 0         | 46             | 0.0            | 0          | 30         
 Reusability      | dct:license                               | 255       | 255            | 1.0            | 20.0       | 20         
 Reusability      | dct:license from vocabulary               | 245       | 255            | 0.96           | 9.61       | 10         
 Reusability      | dct:accessRights                          | 46        | 46             | 1.0            | 10.0       | 10         
 Reusability      | dct:accessRights from vocabulary          | 0         | 46             | 0.0            | 0          | 5          
 Reusability      | dcat:contactPoint                         | 46        | 46             | 1.0            | 20.0       | 20         
 Reusability      | dct:publisher                             | 46        | 46             | 1.0            | 10.0       | 10         
 Contextuality    | dct:rights                                | 255       | 255            | 1.0            | 5.0        | 5          
 Contextuality    | dcat:byteSize                             | 0         | 255            | 0.0            | 0          | 5          
 Contextuality    | dct:issued                                | 46        | 46             | 1.0            | 5.0        | 5          
 Contextuality    | dct:modified                              | 46        | 46             | 1.0            | 5.0        | 5          
 Total points     | Rating: Good                              |           |                | 0.69           | 280.31     | 405        

                              
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
python3 -m pip install --user pipx
pipx install pdm
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


## References
>DCAT-AP:
>  - https://github.com/SEMICeu/DCAT-AP/tree/master/releases
>  - https://semiceu.github.io/DCAT-AP/releases/3.0.0/#validation-of-dcat-ap
>
>EU Vocabularies: https://op.europa.eu/en/web/eu-vocabularies/dcat-ap
>
>Validator: 
>- https://www.itb.ec.europa.eu/shacl/dcat-ap/upload
>-  https://github.com/ISAITB/validator-resources-dcat-ap/tree/master#
>
>DCAT-AP Country profile:
>  - https://github.com/diggsweden/DCAT-AP-SE
>  - https://github.com/opendata-swiss/dcat_ap_ch
>
>SHACLs: https://github.com/ISAITB/validator-resources-dcat-ap/blob/baca3adf63d31ee415fa5e769249053ae211414c/resources/config.properties


### DCAT-AP Validator Validation Cases
The different cases to validate in the [DCAT-AP Validator](https://www.itb.ec.europa.eu/shacl/dcat-ap/upload) are based on the level of completeness of the checks and the incorporation of background knowledge (vocabularies). Each case is designed for a specific data exchange scenario.
The following describes each case and recommends which one you should use for a CKAN catalog:

#### Case 1: DCAT-AP Base Zero (no background knowledge)
Includes all constraints required for technical coherence, excluding range class membership constraints and controlled vocabulary usage.

*SHACL Profiles*: 
* [2.1.1](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_shapes.ttl)
* [3.0.0](https://github.com/SEMICeu/DCAT-AP/blob/master/releases/3.0.0/html/shacl/shapes.ttl)


#### Case 2: DCAT-AP Ranges Zero (no background knowledge)
Includes all range class membership constraints.

*SHACL Profiles*: 
* [2.1.1](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_range.ttl)
* [3.0.0](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/range.ttl)

#### Case 3: DCAT-AP Base (with background knowledge)
Extends Case 1 with background knowledge, including all vocabularies used in DCAT-AP.

*SHACL Profiles*: 
* 2.1.1: [`shapes`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_shapes.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_imports.ttl)
* 3.0.0: [`shapes`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/shapes.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/imports.ttl)

#### Case 4: DCAT-AP Ranges (with background knowledge)
Extends Case 2 with background knowledge, adding validation of range class membership and vocabulary standards compliance.

*SHACL Profiles*:
* 2.1.1: [`range`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_range.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_imports.ttl)
* 3.0.0: [`range`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/range.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/imports.ttl)

#### Case 5: DCAT-AP Recommendations (with background knowledge)
Includes all constraints related to recommended properties.

*SHACL Profiles*: 
* 2.1.1: [`shapes recommended`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_shapes_recommended.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_imports.ttl)
* 3.0.0: [`shapes recommended`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/shapes_recommended.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/imports.ttl)


#### Case 6: DCAT-AP Controlled Vocabularies
Includes all constraints related to controlled vocabularies.

*SHACL Profiles*: 
* 2.1.1: [`vocabularies shape`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_mdr-vocabularies.shape.ttl) and [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_mdr_imports.ttl)
* 3.0.0: [`vocabularies shape`](https://github.com/SEMICeu/DCAT-AP/raw/3.0.0/releases/3.0.0/html/shacl/mdr-vocabularies.shape.ttl) and [`mdr imports`](https://github.com/SEMICeu/DCAT-AP/raw/3.0.0/releases/3.0.0/html/shacl/mdr_imports.ttl)


#### Case 7: DCAT-AP Full (with background knowledge)
The union of Cases 3, 4, 5, and 6.

*SHACL Profiles*: 
* 2.1.1: [`shapes`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_shapes.ttl), [`shapes recommended`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_shapes_recommended.ttl), [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_imports.ttl), [`range`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_range.ttl) and [`deprecateduris`](https://github.com/SEMICeu/DCAT-AP/raw/2.1.1-draft/releases/2.1.1/dcat-ap_2.1.1_shacl_deprecateduris.ttl)
* 3.0.0: [`shapes`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/shapes.ttl), [`shapes recommended`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/shapes_recommended.ttl), [`imports`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/imports.ttl), [`range`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/range.ttl) and [`deprecateduris`](https://github.com/SEMICeu/DCAT-AP/raw/gh-pages/releases/3.0.0-draft/html/shacl/deprecateduris.ttl)


#### Recommendation:
For most use cases, `Case 3: DCAT-AP Base (with background knowledge)` is recommended. It provides comprehensive validation of basic coherence and vocabulary standards compliance.
If your CKAN catalog uses controlled vocabularies, consider using `Case 6: DCAT-AP Controlled Vocabularies` or `Case 7: DCAT-AP Full (with background knowledge)` for more exhaustive validation.
Remember, the choice of the appropriate validation case depends on your specific needs and data exchange context.

## License
Copyright (c) the respective contributors.
It is open and licensed under the GNU Affero General Public License (AGPL) v3.0 whose full text may be found at:
http://www.fsf.org/licensing/licenses/agpl-3.0.html

[^1]: Program to test MQA evaluation: Javier Nogueras (jnog@unizar.es), Javier Lacasta (jlacasta@unizar.es), Manuel Ureña (maurena@ujaen.es), F. Javier Ariza (fjariza@ujaen.es), Héctor Ochoa Ortiz (719509@unizar.es). Trafair Project 2020.
[^2]: A custom installation of Docker Compose with specific extensions for spatial data and [GeoDCAT-AP](https://github.com/SEMICeu/GeoDCAT-AP)/[INSPIRE](https://github.com/INSPIRE-MIF/technical-guidelines) metadata [profiles](https://en.wikipedia.org/wiki/Geospatial_metadata).