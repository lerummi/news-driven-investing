FROM jupyter/minimal-notebook:python-3.11

LABEL maintainer="lerummi <martin.krause.85@gmx.de>"

USER root

# Install apt packages
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install --yes --no-install-recommends \
    graphviz && \
    pip install poetry

USER ${NB_UID}

# Requirements are installed here to ensure they will be cached.
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install Python 3 packages
RUN poetry export -o /tmp/requirements.txt --without-hashes && \
    cat /tmp/requirements.txt

RUN pip install \
    --user \
    --use-deprecated=legacy-resolver \
    -r /tmp/requirements.txt
