#!/bin/bash


type=$1
BASE_URL=$2
fails=""

if  [[ -z "$BASE_URL" ]]; then
        BASE_URL="http://localhost"
fi

inspect() {
  if [[ $1 -ne 0 ]]; then
    fails="${fails} $2"
  fi
}

# run server-side tests
server() {
  docker-compose up -d --build
  docker-compose exec supplyit-users python manage.py test
  inspect $? supplyit-users
  docker-compose exec supplyit-users flake8 project
  inspect $? supplyit-users-lint
  docker-compose down
}


# run client-side tests
client() {
  docker-compose up -d --build
  docker-compose exec client npm run coverage
  inspect $? client
  docker-compose down
}

# run e2e tests
e2e() {
  docker-compose -f docker-compose-prod.yml up -d --build
  docker-compose -f docker-compose-prod.yml exec supplyit-users python manage.py recreate_db
  ./node_modules/.bin/cypress run --config baseUrl=${BASE_URL}
  inspect $? e2e
  docker-compose -f docker-compose-prod.yml down
}

# run all tests
all() {
  docker-compose up -d --build
  docker-compose exec supplyit-users python manage.py test
  inspect $? supplyit-users
  docker-compose exec supplyit-users flake8 project
  inspect $? supplyit-users-lint
  docker-compose exec client npm run coverage
  inspect $? client
  docker-compose down
  e2e
}

# run appropriate tests
if [[ "${type}" == "server" ]]; then
  echo ""
  echo "Running server-side tests!\n"
  server
elif [[ "${type}" == "client" ]]; then
  echo ""
  echo "Running client-side tests!\n"
  client
elif [[ "${type}" == "e2e" ]]; then
  echo ""
  echo "Running e2e tests!\n"
  e2e
else
  echo ""
  echo "Running all tests!\n"
  all
fi

# return proper code
if [ -n "${fails}" ]; then
  echo ""
  echo "Tests failed: ${fails}"
  exit 1
else
  echo ""
  echo "Tests passed!"
  exit 0
fi