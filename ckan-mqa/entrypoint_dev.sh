#!/bin/bash

set -xeuo pipefail

/wait-for --timeout "$TIMEOUT" "$CKAN_CATALOG_URL" -- pdm run python3 -m ptvsd --host 0.0.0.0 --port 5678 --wait ckan2mqa/ckan2mqa.py

exec "$@"
