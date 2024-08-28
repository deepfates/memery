FROM python:3.10.6

RUN mkdir -p /app/images

WORKDIR /app

COPY ./ /app

RUN pip install poetry

RUN poetry install

EXPOSE 8501

CMD ["poetry", "run", "memery", "serve", "/app/images"]
