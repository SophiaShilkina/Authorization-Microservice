# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.14.3
ARG POETRY_VERSION=2.2.1

FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# -------- builder-prod --------
FROM base AS builder-prod

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY src ./src
RUN poetry install --only main --no-interaction --no-ansi

# -------- builder-dev --------
FROM base AS builder-dev

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --with dev --no-interaction --no-ansi --no-root

COPY src ./src
RUN poetry install --with dev --no-interaction --no-ansi

# -------- prod --------
FROM python:${PYTHON_VERSION}-slim-bookworm AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder-prod /usr/local /usr/local
COPY --from=builder-prod /app/src /app/src
COPY --from=avro_contracts . /app/contracts/avro

EXPOSE 8000

CMD ["uvicorn", "root.__main__:app", "--host", "0.0.0.0", "--port", "8000"]

# -------- dev --------
FROM builder-dev AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=avro_contracts . /app/contracts/avro

EXPOSE 8000

CMD ["uvicorn", "root.__main__:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app/src"]