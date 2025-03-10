FROM python:3.12.3-slim AS requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.7.0 || pip install poetry>=1.2.0

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12.3-slim

WORKDIR /work
VOLUME [ "/work" ]

COPY --from=requirements-stage /tmp/requirements.txt /work/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /work/requirements.txt

COPY . /work

WORKDIR /work/app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--port", "8080", "--host", "0.0.0.0"]
