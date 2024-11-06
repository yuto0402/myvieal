# syntax=docker/dockerfile:1

# hadolint global ignore=DL3008,DL3042

ARG BASE_IMAGE=python
ARG PYTHON_VERSION=3.11
ARG DEBIAN_VERSION=bookworm

FROM ${BASE_IMAGE}:${PYTHON_VERSION}-slim-${DEBIAN_VERSION} AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_INSTALLER_MAX_WORKERS=10 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    npm
RUN --mount=type=cache,target=/root/.cache/pip \
    python -c 'from urllib.request import urlopen;exec(urlopen("https://install.python-poetry.org").read())'

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    npm install --production

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    poetry export -o requirements.txt && \
    pip install --no-compile -r requirements.txt && \
    rm requirements.txt

COPY . .

FROM ${BASE_IMAGE}:${PYTHON_VERSION}-slim-${DEBIAN_VERSION}

ARG PYTHON_VERSION

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ARG GID=10001
ARG UID=10001
RUN groupadd -g ${GID} nonroot && \
    useradd -l -M -d /nonexist -s /sbin/nologin -g nonroot -u ${UID} nonroot

RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    libpq5

COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

COPY --from=builder /app .

# pre-compile bytecode for faster startup
RUN python -m compileall -j0 . /usr/local/lib/python${PYTHON_VERSION}

USER nonroot

EXPOSE 8000
CMD ["gunicorn"]
