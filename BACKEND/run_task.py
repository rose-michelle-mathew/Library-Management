from applications.workers import celery_app
from applications.task import hello_world,check_and_send_reminders

if __name__ == "__main__":
    # Trigger the task
    result = check_and_send_reminders.delay()
    print(result.get())
