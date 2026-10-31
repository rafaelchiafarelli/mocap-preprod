# mocap-preprod image: the tests and the agents' MCP server (DEPENDENCIES.md rule B).
# The agents themselves run no Python. Shared Mocap Studio base: Ubuntu 24.04,
# system Python 3.12, pinned by digest; Python deps only from the hashed lockfile.
# The source is not copied in: docker/test.sh mounts the repository.
FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build-py
COPY requirements.lock ./
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --require-hashes -r requirements.lock
# mocap-contracts is not pinned here (DEPENDENCIES.md, mocap-preprod row): docker/test.sh
# passes its newest v* tag, so a new release changes this layer and rebuilds it.
ARG CONTRACTS_TAG
RUN test -n "$CONTRACTS_TAG" \
    && git clone -q --depth 1 --branch "$CONTRACTS_TAG" \
        https://github.com/rafaelchiafarelli/mocap-contracts.git /opt/mocap-contracts \
    && rm -rf /opt/mocap-contracts/.git
# its generated packages ship top-level in gen/python
ENV PYTHONPATH=/opt/mocap-contracts:/opt/mocap-contracts/gen/python \
    MOCAP_CONTRACTS_TAG=$CONTRACTS_TAG
USER ubuntu
WORKDIR /app
