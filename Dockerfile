FROM python:3.11.3-slim
ENV PYTHONUNBUFFERED True
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /app
COPY . /app

RUN poetry config virtualenvs.create false && \
    poetry install -v --no-interaction --no-ansi

EXPOSE 8080
CMD ["gunicorn" ,"--bind", ":8080", "src.main:app"]