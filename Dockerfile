FROM python:3.8.3-alpine3.12
LABEL MAINTAINER Pablo Viojo <pablo@tiopaul.io>

RUN apk add --no-cache gcc g++ python3-dev musl-dev mysql-dev libffi-dev libxml2-dev libc-dev libxslt-dev openssl-dev cargo py3-pep517
RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
RUN export CRYPTOGRAPHY_DONT_BUILD_RUST=1
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src .

CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=12", "--timeout=120", "app:app"]
