
from flask import Blueprint, request, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Cria um novo usuário
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
            - nome
            - email
            - senha
          properties:
            nome:
              type: string
              example: João Silva
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              example: 1234
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Campos obrigatórios ausentes ou e-mail já cadastrado
    """
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    nome  = data.get("nome")

    if not all([email, senha, nome]):
        abort(400, "Campos obrigatórios: email, senha, nome")

    if Usuario.query.filter_by(email=email).first():
        abort(400, "Email já cadastrado")

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=generate_password_hash(senha)  # simples 
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário criado"}), 201


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
    print(email)
    print(senha)
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
