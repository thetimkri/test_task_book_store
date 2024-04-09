FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
    && apt-get install -y graphviz libgraphviz-dev pkg-config

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY book_store/ /code/
