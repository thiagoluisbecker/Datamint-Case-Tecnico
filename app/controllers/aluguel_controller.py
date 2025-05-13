from flask import Blueprint, jsonify, request, abort
from app.repositories.aluguel_repository import AluguelRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.filme_repository import FilmeRepository
from app.factories.aluguel_factory import AluguelFactory
from app.models.aluguel import Aluguel
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
    
    usuario = UsuarioRepository.buscar_por_id(usuario_id)
    filme = FilmeRepository.buscar_por_id(filme_id)

    aluguel = AluguelFactory.criar_aluguel(usuario_id= usuario.id, filme_id = filme.id)
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

    aluguel = AluguelRepository.buscar_por_id(aluguel_id=aluguel_id)
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
    
    usuario = UsuarioRepository.buscar_por_id(usuario_id)
    alugueis_usuario = AluguelRepository.listar_por_usuario(usuario_id=usuario.id)

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