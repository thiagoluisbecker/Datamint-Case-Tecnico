from flask import Blueprint, jsonify, request, abort
from app.models.aluguel import Aluguel
from app.models.usuario import Usuario
from app.models.filme import Filme
from app import db

aluguel_bp = Blueprint('aluguel', __name__)

@aluguel_bp.route('/', methods=['POST'])
def alugar_filme():
    """
    Aluga um filme
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            usuario_id:
              type: integer
              description: ID do usuário
            filme_id:
              type: integer
              description: ID do filme
    responses:
      201:
        description: Filme alugado com sucesso
      400:
        description: Dados inválidos
    """
    dados = request.get_json()
    usuario_id = dados.get('usuario_id')
    filme_id = dados.get('filme_id')

    if not usuario_id or not filme_id:
        abort(400, description="É necessário informar usuario_id e filme_id")
    
    usuario = Usuario.query.get_or_404(usuario_id)
    filme = Filme.query.get_or_404(filme_id)

    aluguel = Aluguel(usuario= usuario, filme = filme)
    db.session.add(aluguel)
    db.session.commit()

    return jsonify({'mensagem':'Filme alugado com sucesso', 'aluguel_id':aluguel.id}), 201


@aluguel_bp.route('/<int:aluguel_id>/avaliar', methods=['POST'])
def avaliar_filme(aluguel_id):
    """
    Avalia filme alugado
    ---
    parameters:
      - name: aluguel_id
        in: path
        type: integer
        required: true
        description: ID do aluguel
      - name: body
        in: body
        required: true
        schema:
          properties:
            nota:
              type: number
              format: float
              description: Nota de 0 a 10
    responses:
      200:
        description: Nota registrada
      400:
        description: Nota inválida
      404:
        description: Aluguel não encontrado
    """
    dados = request.get_json()
    nota = dados.get('nota')

    if not nota or nota>10 or nota<0:
        abort(400, description="Nota inválida, ela deve ser de 0 a 10")

    aluguel = Aluguel.query.get_or_404(aluguel_id)
    aluguel.nota = nota
    db.session.commit()

    return jsonify({'mensagem': f'Nota {nota} registrada para o aluguel {aluguel.id}'}), 200 


@aluguel_bp.route('usuario/<int:usuario_id>/', methods=['GET'])
def lista_alugueis_usuario(usuario_id):
    """
    Listar todos os filmes alugados de um usuário
    ---
    parameters:
      - name: usuario_id
        in: path
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Lista de alugueis
      404:
        description: Usuário não encontrado
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    alugueis_usuario = Aluguel.query.filter_by(usuario_id = usuario.id).all()

    lista_alugueis_usuario = []
    for aluguel in alugueis_usuario:
        dados_aluguel = {
            'filme_id':aluguel.filme.id,
            'filme_nome':aluguel.filme.nome,
            'nota':aluguel.nota,
            'data_locacao':aluguel.data_locacao,
        }
        lista_alugueis_usuario.append(dados_aluguel)


    return jsonify(lista_alugueis_usuario)