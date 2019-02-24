from celery_tasks.main import celery

@ celery.task(name='send_email')
def send_email():
    pass