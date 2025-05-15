import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flasgger import Swagger
from flask_caching import Cache

from .extensions import db, login_manager          # único login_manager
from app.models.usuario import Usuario             # importa modelo aqui

migrate = Migrate()
cache   = Cache()


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(Usuario, int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"erro": "Login necessário"}), 401


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # ---------- Configurações ----------
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.getenv(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE='SimpleCache',
        CACHE_DEFAULT_TIMEOUT=300,
    )
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    os.makedirs(app.instance_path, exist_ok=True)

    # ---------- Extensões ----------
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    Swagger(app)

    # ---------- Modelos e blueprints ----------
  
    from app.models import usuario, filme, genero, aluguel
    from app.controllers.filme_controller   import filme_bp
    from app.controllers.aluguel_controller import aluguel_bp
    from app.controllers.auth_controller    import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(filme_bp,   url_prefix="/filmes")
    app.register_blueprint(aluguel_bp, url_prefix="/alugueis")

    return app
