FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/Auction-app/.venv/bin:/root/.local/bin"

RUN mkdir /Auction-app

WORKDIR /Auction-app

COPY pyproject.toml poetry.lock .
RUN poetry install --no-dev --no-root

COPY . .
