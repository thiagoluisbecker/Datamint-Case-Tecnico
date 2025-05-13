from flask import Blueprint, jsonify
from app.models.filme import Filme
from app.repositories.filme_repository import FilmeRepository
from app import db

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/', methods=['GET'])
def get_filmes():
    filmes = FilmeRepository.listar_todos()
    if not filmes:
        return jsonify({'mensagem': f'Nenhum filme encontrado'}), 404
    
    lista_filmes = []
    for filme in filmes:
        lista_filmes.append({
            'id': filme.id,
            'nome': filme.nome,
            'genero': filme.genero,
            'sinopse': filme.sinopse,
            'diretor': filme.diretor,
            'ano': filme.ano,
        })

    return jsonify(lista_filmes), 200



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
        'genero':filme.genero,
        'sinopse':filme.sinopse,
        'diretor':filme.diretor,
        'ano':filme.ano,
    }

    return jsonify(dados_filme), 200



@filme_bp.route('/genero/<genero>', methods=['GET'])
def get_filmes_por_genero(genero):
    """
    Lista filmes por gênero
    ---
    parameters:
      - name: genero
        in: path
        type: string
        required: true
        description: Gênero do filme
    responses:
      200:
        description: Lista de filmes encontrados
      404:
        description: Nenhum filme encontrado
    """
    filmes = FilmeRepository.listar_por_genero(genero)
    if not filmes:
        return jsonify({'mensagem': f'Nenhum filme encontrado no gênero: {genero}'}), 404


    lista_filmes = []
    for filme in filmes:
        lista_filmes.append({
            'id': filme.id,
            'nome': filme.nome,
            'genero': filme.genero,
            'sinopse': filme.sinopse,
            'diretor': filme.diretor,
            'ano': filme.ano,
        })


    return jsonify(lista_filmes), 200