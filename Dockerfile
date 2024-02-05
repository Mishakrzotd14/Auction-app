FROM python:3.11

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="${PATH}:/root/.local/bin"

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

RUN mkdir /Auction-app

WORKDIR /Auction-app

COPY pyproject.toml poetry.lock /Auction-app/
RUN poetry config virtualenvs.create false && \
    poetry install

# Копируем остальные файлы проекта
COPY . /Auction-app/
