#!/bin/bash


env=$1
fails=""

if  [[ -z "$BASE_URL" ]]; then
        BASE_URL="http://localhost"
fi

inspect() {
  if [[ $1 -ne 0 ]]; then
    fails="${fails} $2"
  fi
}

# run client and server-side tests
dev() {
  docker-compose up -d --build
  docker-compose exec supplyit-users python manage.py test
  inspect $? supplyit-users
  docker-compose exec supplyit-users flake8 project
  inspect $? supplyit-users-lint
  # docker-compose exec client npm i enzyme
  docker-compose exec client npm run coverage
  inspect $? client
  docker-compose down
}

# run e2e tests
e2e() {
  docker-compose -f docker-compose-$1.yml up -d --build
  docker-compose -f docker-compose-$1.yml run supplyit-users python manage.py recreate_db
  ./node_modules/.bin/cypress run --config baseUrl=${BASE_URL}
  inspect $? e2e
  docker-compose -f docker-compose-$1.yml down
}

# run appropriate tests
if [[ "${env}" == "development" ]]; then
  echo "Running client and server-side tests!"
  dev
elif [[ "${env}" == "staging" ]]; then
  echo "Running e2e tests!"
  e2e stage
elif [[ "${env}" == "production" ]]; then
  echo "Running e2e tests!"
  e2e prod
else
  echo "Running client and server-side tests!"
  dev
fi

# return proper code
if [[ -n "${fails}" ]]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi