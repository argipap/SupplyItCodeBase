import os
import random

import celery

from project.utils.mailgun import Mailgun, MailGunException

CELERY_BROKER = os.environ.get("CELERY_BROKER")
CELERY_BACKEND = os.environ.get("CELERY_BACKEND")

celery_app = celery.Celery("tasks", broker=CELERY_BROKER, backend=CELERY_BACKEND)


@celery_app.task(
    bind=True, retry_kwargs={"max_retries": 3},
)
def send_async_mail_task(self, email, subject, text, html):
    try:
        resp = Mailgun.send_email([email], subject, text, html)
        return resp.json()
    except MailGunException as e:
        self.retry(exc=e, countdown=int(random.uniform(2, 4) ** self.request.retries))
