# project/tests/maislurp_lib.py

import mailslurp_client
from mailslurp_client.rest import ApiException
from flask import current_app


class MailSlurpClient:
    INBOX_ID = "79a7f01e-cd8e-4071-8b40-5fd016d311de"
    CONFIGURATION = mailslurp_client.Configuration()
    CONFIGURATION.api_key["x-api-key"] = current_app.config["MAILSLURP_API_KEY"]

    @classmethod
    def mailslurp_wait_for_latest_email(cls, configuration):
        with mailslurp_client.ApiClient(configuration) as api_client:
            api_instance = mailslurp_client.WaitForControllerApi(api_client)
            inbox_id = cls.INBOX_ID
            timeout = 10000
            try:
                api_response = api_instance.wait_for_latest_email(
                    inbox_id=inbox_id, timeout=timeout, unread_only=False
                )
                return api_response
            except ApiException as e:
                print(
                    "Exception calling WaitForControllerApi->wait_for_latest_email: %s"
                    % e
                )
        return False

    @classmethod
    def mailslurp_empty_inbox(cls, configuration):
        with mailslurp_client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = mailslurp_client.CommonActionsControllerApi(api_client)

            try:
                # Delete all emails in an inbox
                api_instance.empty_inbox(cls.INBOX_ID)
            except ApiException as e:
                print(
                    "Exception calling CommonActionsControllerApi->empty_inbox: %s" % e
                )
