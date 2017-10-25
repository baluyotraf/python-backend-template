from time import sleep
from flask import current_app
from app.extensions import celery

@celery.task(bind=True)
def sample_task(self):
    limit = 10
    for i in range(limit):
        self.update_state(state='PROGRESS', meta={'current':i})
        sleep(1)
    return {'current':limit}
