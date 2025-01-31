FROM python:3.11.11-bullseye

ARG FOR_DEVELOPMENT=true
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app


# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

# Allow installing dev dependencies to run tests
COPY ./src /app

RUN bash -c "if [ $FOR_DEVELOPMENT == 'true' ] ; then poetry install; else poetry install --no-dev ; fi"
