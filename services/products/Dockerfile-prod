# base image
FROM python:3.7.2-slim

RUN apt-get update -yqq \
&& apt-get install -yqq --no-install-recommends \
netcat \
&& apt-get -q clean \
&& pip install --upgrade pip

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./Pipfile /usr/src/app
COPY ./Pipfile.lock /usr/src/app
RUN pip install pipenv \
&& pipenv lock -r > /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]
