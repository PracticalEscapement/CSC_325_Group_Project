from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate

import os


db =SQLAlchemy()
DB_NAME ="database.db"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    # app.config['SECRET_KEY'] = 'ok30vXjg5n'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'


    db.init_app(app)
    migrate = Migrate(app, db)


    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User

    create_database(app)

    from .Routes.Comments import comments_routes
    from .Routes.Communities import community_routes
    from .Routes.messages import Messages_routes
    from .Routes.Notifications import Notifications_routes
    from .Routes.Users import Users_routes
    from .Routes.Posts import Posts_routes
    
    app.register_blueprint(comments_routes)
    app.register_blueprint(community_routes)
    app.register_blueprint(Messages_routes)
    app.register_blueprint(Notifications_routes)
    app.register_blueprint(Users_routes)
    app.register_blueprint(Posts_routes)


    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()

        