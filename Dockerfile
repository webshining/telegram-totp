FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libzbar0

RUN pip install virtualenv

RUN virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libzbar0

ENV PATH="/opt/venv/bin:$PATH"

COPY .. .

RUN chmod +x ./bin/entrypoint.sh

ENTRYPOINT ["./bin/entrypoint.sh"]