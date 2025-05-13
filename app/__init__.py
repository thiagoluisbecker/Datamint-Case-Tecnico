import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

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

    Swagger(app)

    from app.models import filme, usuario, aluguel, genero
    from app.controllers.filme_controller import filme_bp
    from app.controllers.aluguel_controller import aluguel_bp
    app.register_blueprint(filme_bp, url_prefix='/filmes')
    app.register_blueprint(aluguel_bp, url_prefix='/alugueis')
    
    
    return app
