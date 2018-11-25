FROM python:3.6-alpine

RUN apk add --no-cache bash gcc build-base zeromq

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5556
EXPOSE 5566

CMD make start-server
