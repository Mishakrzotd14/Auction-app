FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Auction-app

COPY pyproject.toml poetry.lock /Auction-app/
RUN poetry config virtualenvs.create false && \
    poetry install

COPY . /Auction-app/
