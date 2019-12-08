#!/bin/sh

inspect() {
  if [[ $1 -ne 0 ]]; then
    echo "{$2} failed"
    fails="${fails} $2"
  fi
}

if [[ -z "$TRAVIS_PULL_REQUEST" ]] || [[ "$TRAVIS_PULL_REQUEST" == "false" ]]
then

  if [[ "$TRAVIS_BRANCH" == "staging" ]]; then
    export DOCKER_ENV=stage
    export REACT_APP_USERS_SERVICE_URL="http://supplyit-staging-alb-471661531.us-east-1.elb.amazonaws.com"
  elif [[ "$TRAVIS_BRANCH" == "production" ]]; then
    export DOCKER_ENV=prod
  fi

  if [[ "$TRAVIS_BRANCH" == "staging" ]] || \
     [[ "$TRAVIS_BRANCH" == "production" ]]
  then
    curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
    unzip awscli-bundle.zip
    ./awscli-bundle/install -b ~/bin/aws
    export PATH=~/bin:$PATH
    # add AWS_ACCOUNT_ID, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY env vars
    eval $(aws ecr get-login --region us-east-1 --no-include-email)
    export TAG=$TRAVIS_BRANCH
    export REPO=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
  fi

  if [[ "$TRAVIS_BRANCH" == "staging" ]] || \
     [[ "$TRAVIS_BRANCH" == "production" ]]
  then
    echo "building/pushing USERS_REPO: ${USERS_REPO} for env: {$DOCKER_ENV} ..."
    # users
    docker build $USERS_REPO -t $USERS:$COMMIT -f Dockerfile-$DOCKER_ENV
    inspect $? users_docker_build
    docker tag $USERS:$COMMIT $REPO/$USERS:$TAG
    inspect $? users_docker_tag
    docker push $REPO/$USERS:$TAG
    inspect $? users_docker_push
    # users db
    docker build $USERS_DB_REPO -t $USERS_DB:$COMMIT -f Dockerfile
    inspect $? usersdb_docker_build
    docker tag $USERS_DB:$COMMIT $REPO/$USERS_DB:$TAG
    inspect $? usersdb_docker_tag
    docker push $REPO/$USERS_DB:$TAG
    inspect $? usersdb_docker_push
    # client
    docker build $CLIENT_REPO -t $CLIENT:$COMMIT -f Dockerfile-$DOCKER_ENV --build-arg REACT_APP_USERS_SERVICE_URL=$REACT_APP_USERS_SERVICE_URL
    inspect $? client_docker_build
    docker tag $CLIENT:$COMMIT $REPO/$CLIENT:$TAG
    inspect $? client_docker_tag
    docker push $REPO/$CLIENT:$TAG
    inspect $? client_docker_push
    # swagger
    docker build $SWAGGER_REPO -t $SWAGGER:$COMMIT -f Dockerfile-$DOCKER_ENV
    inspect $? swagger_docker_build
    docker tag $SWAGGER:$COMMIT $REPO/$SWAGGER:$TAG
    inspect $? swagger_docker_tag
    docker push $REPO/$SWAGGER:$TAG
    inspect $? swagger_docker_push

    # return proper code
    if [[ -n "${fails}" ]]; then
        echo "Docker push image failed: ${fails}"
        exit 1
    else
        echo "Docker push image suceeded!"
        exit 0
    fi
  fi
fi