FROM node:11.12.0-alpine

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json
RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++

RUN npm ci
# To handle 'not get uid/gid'
RUN npm config set unsafe-perm true
RUN npm install react-scripts@2.1.8 -g --silent

RUN apk del .gyp

# start app
CMD ["npm", "start"]