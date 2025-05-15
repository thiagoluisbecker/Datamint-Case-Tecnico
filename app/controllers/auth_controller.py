
from flask import Blueprint, request, jsonify, abort
from flask_login import login_user, logout_user, login_required
from app.models.usuario import Usuario
from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Efetua login e cria a sessão
    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
              example: thiagobeckerrocha@gmail.com
            senha:
              type: string
              example: teste_thiago
    responses:
      200:
        description: Login bem-sucedido (cookie de sessão gravado)
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Login OK
            usuario_id:
              type: integer
              example: 1
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
  
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.senha, senha):
        abort(401, "Credenciais inválidas")

    login_user(usuario)                    # cria a sessão (cookie secure)
    return jsonify({"mensagem": "Login OK", "usuario_id": usuario.id})


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Encerra a sessão do usuário logado
    ---
    tags:
      - Autenticação
    responses:
      200:
        description: Logout realizado com sucesso
      401:
        description: Usuário não autenticado
    """
    logout_user()
    return jsonify({"mensagem": "Logout OK"})
