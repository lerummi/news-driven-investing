FROM python:3.11-slim

# Checkout and install dagster libraries needed to run the gRPC server
# exposing your repository to dagit and dagster-daemon, and to load the DagsterInstance

# Install apt packages
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y wget && \
    apt-get install --yes --no-install-recommends \
    graphviz && \
    pip install poetry && \
    rm -rf /var/lib/apt/lists/*


# Requirements are installed here to ensure they will be cached.
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install Python 3 packages
RUN poetry export -o /tmp/requirements.txt --without-hashes && \
    cat /tmp/requirements.txt

RUN pip install --use-deprecated=legacy-resolver  -r /tmp/requirements.txt

WORKDIR /opt/dagster/app

