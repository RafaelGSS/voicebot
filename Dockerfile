FROM python:3
EXPOSE 5000

RUN apt install -y curl python3 python openssl libffi-dev  make gcc g++ \
    && mkdir -p /app

WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt \
    && pip install uwsgi

ADD . /app/

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
