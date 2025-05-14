from flask import Blueprint, jsonify, request, abort
from app.repositories.aluguel_repository import AluguelRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.filme_repository import FilmeRepository
from app.factories.aluguel_factory import AluguelFactory
from app.models.aluguel import Aluguel
from app import db


aluguel_bp = Blueprint('aluguel', __name__)

@aluguel_bp.route('/', methods=['POST']) #passar so o filme
def alugar_filme():
    """
    Usuário aluga um filme
    ---
    parameters:
      - name: X-User-Id
        in: header
        type: integer
        required: true
        description: ID do usuário autenticado (simulação)
      - name: filme_id
        in: body
        required: true
        schema:
          properties:
            filme_id:
              type: integer
              description: ID do filme
    responses:
      200:
        description: Filme alugado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Filme não encontrado
    """
    dados = request.get_json()
    filme_id = dados.get('filme_id')

    
    usuario_id = request.headers.get('X-User-Id', type=int)
    if not usuario_id or not filme_id:
        abort(400, description="É necessário informar filme_id e estar autenticado via X-User-Id")

    usuario = UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        abort(404, description="Usuário não encontrado.")

    filme = FilmeRepository.buscar_por_id(filme_id)
    if not filme:
        abort(404, description="Filme não encontrado.")

    aluguel = AluguelFactory.criar_aluguel(usuario_id=usuario.id, filme_id=filme.id)
    db.session.add(aluguel)
    db.session.commit()

    return jsonify({'mensagem': 'Filme alugado com sucesso', 'aluguel_id': aluguel.id}), 200


@aluguel_bp.route('/meus-alugueis/avaliar/<int:aluguel_id>', methods=['POST']) # id do filme, pq ja tenho id do usuario
def avaliar_filme_alugado(aluguel_id):
    """
    Avalia filme alugado por um usuário
    ---
    parameters:
      - name: X-User-Id
        in: header
        type: integer
        required: true
        description: ID do usuário autenticado (simulação)
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
      403:
        description: Permissão inválida para avaliar o aluguel
      404:
        description: Aluguel não encontrado
    """
    dados = request.get_json()
    nota = dados.get('nota')

    usuario_id = request.headers.get('X-User-Id', type=int)

    if nota is None or nota < 0 or nota > 10:
        abort(400, description="Nota inválida. Deve ser entre 0 e 10.")

    aluguel = AluguelRepository.buscar_por_id(aluguel_id)
    if not aluguel:
        abort(404, description="Aluguel não encontrado.")

    if aluguel.nota is not None:
        abort(400, description="Esse aluguel já foi avaliado.")

    if aluguel.usuario_id != usuario_id:
        abort(403, description="Você não tem permissão para avaliar este aluguel")


    aluguel.nota = nota

    filme = aluguel.filme
    filme.total_avaliacoes += 1
    filme.nota_final = ((filme.nota_final * (filme.total_avaliacoes - 1)) + nota) / filme.total_avaliacoes

    db.session.commit()

    return jsonify({'mensagem': f'Nota {nota} registrada para o aluguel {aluguel.id} e filme atualizado.'}), 200


@aluguel_bp.route('/meus-alugueis', methods=['GET'])
def lista_alugueis_usuario():
    """
    Lista filmes alugados do usuário
    ---
    parameters:
      - name: X-User-Id
        in: header
        type: integer
        required: true
        description: ID do usuário autenticado (simulação)
    responses:
      200:
        description: Lista de alugueis
      400:
        description: O usuário deve estar autenticado via X-User-Id
      404:
        description: Usuário não encontrado
    """
    
    usuario_id = request.headers.get('X-User-Id', type=int)
    if not usuario_id:
        abort(400, description="O usuário deve estar autenticado via X-User-Id")

    usuario = UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        abort(404, description="Usuário não encontrado.")

    alugueis_usuario = AluguelRepository.listar_por_usuario(usuario_id=usuario.id)
    if not alugueis_usuario:
        abort(404, description="Aluguel nâo encontrado.")
        
    lista_alugueis_usuario = [{
        'filme_nome': aluguel.filme.nome,
        'nota': aluguel.nota,
        'data_locacao': aluguel.data_locacao,
    } for aluguel in alugueis_usuario]

    return jsonify(lista_alugueis_usuario)
