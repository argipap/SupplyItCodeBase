#!/bin/sh

if [ -z "$TRAVIS_PULL_REQUEST" ] || [ "$TRAVIS_PULL_REQUEST" == "false" ]
then

  if [ "$TRAVIS_BRANCH" == "production" ]
  then

    JQ="jq --raw-output --exit-status"

    configure_aws_cli() {
        aws --version
        aws configure set default.region us-east-1
        aws configure set default.output json
        echo "AWS Configured!"
    }

    register_definition() {
      if revision=$(aws ecs register-task-definition --cli-input-json "$task_def" | $JQ '.taskDefinition.taskDefinitionArn'); then
        echo "Revision: $revision"
      else
        echo "Failed to register task definition"
        return 1
      fi
    }

    update_service() {
      if [[ $(aws ecs update-service --cluster $cluster --service $service --task-definition $revision | $JQ '.service.taskDefinition') != $revision ]]; then
        echo "Error updating service: ${service}."
        return 1
      fi
    }

    deploy_cluster() {

      cluster="supplyit-production-cluster"

      # users
      service="supplyit-users-prod-service"
      template="ecs_users_prod_taskdefinition.json"
      task_template=$(cat "ecs/$template")
      task_def=$(printf "$task_template" $AWS_ACCOUNT_ID $AWS_RDS_URI $PRODUCTION_SECRET_KEY $AWS_ACCOUNT_ID $AWS_ACCOUNT_ID $MAILGUN_API_KEY $MAILGUN_DOMAIN $AWS_ACCOUNT_ID)
      echo "$task_def"
      register_definition
      # update users service with the new task definitions
      update_service

      # client
      service="supplyit-client-prod-service"
      template="ecs_client_prod_taskdefinition.json"
      task_template=$(cat "ecs/$template")
      task_def=$(printf "$task_template" $AWS_ACCOUNT_ID)
      echo "$task_def"
      register_definition
      # update client service with the new task definitions
      update_service

      # swagger
      service="supplyit-swagger-prod-service"
      template="ecs_swagger_prod_taskdefinition.json"
      task_template=$(cat "ecs/$template")
      task_def=$(printf "$task_template" $AWS_ACCOUNT_ID)
      echo "$task_def"
      register_definition
      # update users swagger with the new task definitions
      update_service

    }

    configure_aws_cli
    deploy_cluster

  fi

fi