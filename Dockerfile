FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PROJECT_NAME=snippets_test

WORKDIR /code

COPY entrypoint.sh /code
COPY . /code 

RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev libpq-dev python3-dev gcc jq unzip libc-dev \
    build-essential && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]