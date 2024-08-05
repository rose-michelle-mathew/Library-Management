from celery import Celery, Task
from flask import Flask 

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    # Initialize Celery app
    celery_app = Celery(app, task_cls=FlaskTask)
    celery_app.config_from_object("celeryconfig")
    return celery_app

# # Initialize Flask app
# app = Flask(__name__)
# app.config.from_pyfile('config.py')

# # Initialize Celery with Flask app
# celery_app = celery_init_app(app)
