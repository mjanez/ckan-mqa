#!/bin/bash

set -xeuo pipefail

/wait-for --timeout "$TIMEOUT" "$CKAN_CATALOG_URL" -- pdm run python3 ckan2mqa/ckan2mqa.py

exec "$@"
