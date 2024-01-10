FROM python:3.11-slim-buster AS build

ENV POETRY_HOME=/etc/poetry

RUN apt-get update && apt-get install --no-install-recommends -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /build
COPY . .

RUN $POETRY_HOME/venv/bin/poetry install
RUN $POETRY_HOME/venv/bin/poetry run pytest
RUN $POETRY_HOME/venv/bin/poetry build


FROM python:3.11-slim-buster

COPY --from=build /build/dist/lightfm-0.1.0.tar.gz /app/pkg/

WORKDIR /app

RUN pip install /app/pkg/lightfm-0.1.0.tar.gz

CMD ["gunicorn", "lightfm.main:app", "--bind" , "0.0.0.0:8080", "--workers",  "1"]