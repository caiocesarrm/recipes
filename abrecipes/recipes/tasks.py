from celery import task, shared_task

@shared_task(bind=True)
def send_email(self, recipe):
    try:
        #send email code, could be when a new recipe is created, etc...
        pass
    except Exception as e:
        return str(e)
    return {'success':True, 'task_uuid':self.request.id}