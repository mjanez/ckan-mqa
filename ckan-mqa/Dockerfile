FROM python:3.11-slim
LABEL maintainer="mnl.janez@gmail.com"

ENV APP_DIR=/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone
ENV CKAN_CATALOG_URL=http://localhost:5000/catalog.rdf
ENV DCATAP_FILES_VERSION=2.1.1
ENV DEV_MODE=False
ENV TIMEOUT=20

RUN apt-get -q -y update && \
    apt-get install -y --no-install-recommends wget=1.21.3-1+b2 gettext-base=0.21-12 && \
    rm -rf /var/lib/apt/lists/* && \
    wget --progress=dot:giga -O /wait-for https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for && \
    chmod +x /wait-for && \
    python3 -m pip install --no-cache-dir pdm==2.12.3

WORKDIR ${APP_DIR}
COPY pyproject.toml pdm.lock ./

RUN pdm install --no-self --group prod

COPY ckan-mqa/docker-entrypoint.d/entrypoint.sh entrypoint.sh
COPY ckan2mqa ckan2mqa

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]