from flask import Flask
from.views import views

def create_app():
    app = Flask(__name__)
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app