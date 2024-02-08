#!/bin/bash

set -xeuo pipefail

pdm run python3 ckan2mqa/ckan2mqa.py

exec "$@"
