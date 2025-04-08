from celery import Celery, Task
from flask import Flask
from flask_static_digest import FlaskStaticDigest
from flask_session import Session
from secrets import token_urlsafe
from flask_talisman import Talisman

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config.get("CELERY_CONFIG",{}))
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app() -> Flask:
    app = Flask(__name__,static_folder="../public",static_url_path="")
    app.config.from_object("config.settings")
    app.secret_key = token_urlsafe()
    celery_init_app(app)
    # Talisman(app) #breaks inline script, needs to be configured some how but idfk what
    Session(app)
    FlaskStaticDigest(app)
    return app