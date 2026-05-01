FROM python:3.10-slim

ENV PIP_INDEX_URL="https://mirrors.huaweicloud.com/repository/pypi/simple/"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . .