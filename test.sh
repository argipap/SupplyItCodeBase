#!/bin/bash


fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run unit and integration tests
docker-compose up -d --build
docker-compose exec supplyit-users python manage.py test
inspect $? supplyit-users
docker-compose exec supplyit-users flake8 project
inspect $? supplyit-users-lint
docker-compose exec client npm run coverage
inspect $? client
docker-compose down

# new
# run e2e tests
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose -f docker-compose-prod.yml exec supplyit-users python manage.py recreate_db
./node_modules/.bin/cypress run --config baseUrl=http://localhost
inspect $? e2e
docker-compose -f docker-compose-prod.yml down

# return proper code
if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi