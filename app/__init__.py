import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'filmes.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://filmes_user:postgres@localhost:5432/filmes_api'


    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)


    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
