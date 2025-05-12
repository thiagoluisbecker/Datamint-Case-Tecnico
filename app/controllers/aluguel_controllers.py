from flask import Blueprint, jsonify, request, abort
from app.models.aluguel import Aluguel
from app.models.usuario import Usuario
from app.models.filme import Filme
from app import db
from datetime import datetime

aluguel_bp = Blueprint('aluguel', __name__)

@aluguel_bp.route('/', methods=['POST'])
def alugar_filme():
    dados = request.get_json()
    usuario_id = dados.get('usuario_id')
    filme_id = dados.get('filme_id')

    if not usuario_id or not filme_id:
        abort(400, description="É necessário informar usuario_id e filme_id")
    
    usuario = Usuario.query.get_or_404(usuario_id)
    filme = Filme.query.get_or_404(filme_id)

    aluguel = Aluguel(usuario= usuario.id, filme = filme.id)
    db.session.add(aluguel)
    db.session.commit()

    return jsonify({'mensagem':'Filme alugado com sucesso', 'alguel_id':aluguel.id}), 200


@aluguel_bp.route('/<int:aluguel_id>/avaliar', methods=['POST'])
def avaliar_filme(aluguel_id):
    dados = request.get_json()
    nota = dados.get('nota')

    if not nota or nota>10 and nota<0:
        abort(400, description="Nota inválida, ela deve ser de 0 a 10")

    aluguel = Aluguel.query.get_or_404(aluguel_id)
    aluguel.nota = nota
    db.session.commit()

    return jsonify({'mensagem': f'Nota {nota} registrada para o aluguel {aluguel.id}'})


@aluguel_bp.route('/<int:usuario_id>/alugueis', methods=['GET'])
def lista_alugueis_usuario(usuario_id):
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