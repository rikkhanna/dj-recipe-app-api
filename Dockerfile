FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
# apk is package manager
# --update means update the registry before we add it
# don't store the registry index on our docker file and we do this to minimize
# the number of extra files and packages that are included in 
# our docker container


# install some temp packages that will run on system while we run our 
# requirements and remove them after
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# delete temp requirements
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

