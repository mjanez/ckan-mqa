FROM python:3.13.0a3-slim
LABEL maintainer="mnl.janez@gmail.com"

ENV APP_DIR=/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone
ENV CKAN_CATALOG_URL=http://localhost:5000/catalog.rdf
ENV DCATAP_FILES_VERSION=2.1.1
ENV DEV_MODE=False
ENV TIMEOUT=20

RUN apt-get -q -y update && \
    apt-get install -y wget && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq install gettext-base && \
    wget -O /wait-for https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for && \
    chmod +x /wait-for && \
    python3 -m pip install pdm

WORKDIR ${APP_DIR}
COPY pyproject.toml pdm.lock .

RUN pdm install --no-self --group prod

COPY ckan-mqa/entrypoint.sh entrypoint.sh
COPY ckan2mqa ckan2mqa

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]