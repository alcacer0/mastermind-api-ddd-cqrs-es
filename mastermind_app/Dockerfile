FROM python:3.8.3-alpine

# Directory inside the container
WORKDIR /mastermind-api/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add postgresql-dev && \
    apk add --virtual build-deps gcc musl-dev libffi-dev make

RUN pip install --upgrade pip
# Copy requirements file to /mastermind-api/pip_requirements.txt
COPY pip_requirements.txt pip_requirements.txt
# And install requirements. Before copying all source code to avoid invalidating this cache layer.
RUN pip install -r pip_requirements.txt

COPY . .
