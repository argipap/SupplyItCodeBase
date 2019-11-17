# base image
FROM python:3.7.2

# create and set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


RUN apt-get update -yqq \
&& apt-get install -yqq --no-install-recommends \
netcat \
&& apt-get -q clean

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]