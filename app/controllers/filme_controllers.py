from flask import Blueprint, jsonify
from app.models.filme import Filme
from app import db

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/', methods=['GET'])
def get_filmes():
    filmes = Filme.query.all()
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
    filme = Filme.query.get_or_404(filme_id)
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
    filmes = Filme.query.filter_by(genero=genero).all()
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