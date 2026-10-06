FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY metadata ./metadata

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

ENTRYPOINT ["tillerbase"]
CMD ["validate", "metadata/datasets.tsv"]
