from flask import Blueprint, jsonify
from app.repositories.filme_repository import FilmeRepository
from app import cache

filme_bp = Blueprint('filme', __name__)


@filme_bp.route('/<int:filme_id>', methods=['GET'])
def get_filme_por_id(filme_id):
    """
    Lista todas as informações sobre um determinado filme
    ---
    parameters:
      - name: filme_id
        in: path
        type: integer
        required: true
        description: ID do filme
    responses:
      200:
        description: Detalhes do filme encontrado
      404:
        description: Filme não encontrado
    """

    filme = FilmeRepository.buscar_por_id(filme_id)
    if not filme:
        return jsonify({'mensagem': f'Nenhum filme encontrado com o id {filme_id}'}), 404
    
    dados_filme = {
        'id':filme.id,
        'nome':filme.nome,
        'genero':filme.genero.nome,
        'sinopse':filme.sinopse,
        'diretor':filme.diretor,
        'ano':filme.ano,
    }

    return jsonify(dados_filme), 200



@filme_bp.route('/genero/<int:genero_id>', methods=['GET'])
@cache.cached(timeout=300, key_prefix='filmes_por_genero')
def get_filmes_por_genero(genero_id):
    """
    Lista os filmes por ID do gênero
    ---
    parameters:
      - name: genero_id
        in: path
        type: integer
        required: true
        description: ID do gênero do filme
    responses:
      200:
        description: Lista de filmes encontrados para o gênero
      404:
        description: Nenhum filme com o gênero encontrado
    """
    filmes = FilmeRepository.listar_por_genero_id(genero_id)
    if not filmes:
        return jsonify({'mensagem': f'Nenhum filme encontrado para o gênero ID: {genero_id}'}), 404

    lista_filmes = [{
        'id': filme.id,
        'nome': filme.nome,
        'genero': filme.genero.nome,
        'sinopse': filme.sinopse,
        'diretor': filme.diretor,
        'ano': filme.ano,
    } for filme in filmes]

    return jsonify(lista_filmes), 200