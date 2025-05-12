from flask import Blueprint, jsonify
from app.models.filme import Filme
from app import db

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/', methods=['GET'])
def get_filmes():
    filmes = Filme.query.all()
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
    dados_filme = {
        'id':filme.id,
        'nome':filme.nome,
        'genero':filme.genero,
        'sinopse':filme.sinopse,
        'diretor':filme.diretor,
        'ano':filme.ano,
    }

    return jsonify(dados_filme), 200



    