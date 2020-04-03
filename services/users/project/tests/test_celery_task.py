import unittest
from project.utils import tasks
from unittest.mock import patch


class TestCeleryTasks(unittest.TestCase):
    @patch("project.utils.tasks.send_async_mail_task")
    def test_send_async_mail_task(self, mock_task):
        mock_task.run.return_value = {
            "id": "<9999999999.1.ZZZZZZZZZZZZZ@sandboxXXXXXXXXXXXXXXXXX.mailgun.org>",
            "message": "Queued. Thank you.",
        }
        email = "argipapaefstathiou@gmail.com"
        subject = "test celery asnyc mail"
        text = "Please click the link to confirm your registration: #"
        html = (
            f"<html>Please click the link to confirm your registration:"
            f"<a href=#>link</a></html>"
        )
        data = tasks.send_async_mail_task.run(
            email=email, subject=subject, text=text, html=html
        )
        self.assertIn(
            "mailgun", data["id"],
        )
        self.assertIn(
            "Queued. Thank you.", data["message"],
        )


if __name__ == "__main__":
    unittest.main()
