from flask import Blueprint, jsonify, request, abort
from app.repositories.aluguel_repository import AluguelRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.filme_repository import FilmeRepository
from app.factories.aluguel_factory import AluguelFactory
from flask_login import login_required, current_user
from app.extensions import db

aluguel_bp = Blueprint('aluguel', __name__)

@aluguel_bp.route('/', methods=['POST']) 
@login_required
def alugar_filme():
    """
    Usuário aluga um filme
    ---
    parameters:
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
      401:
        description: Usuário não autenticado
      404:
        description: Filme não encontrado
    """
    dados = request.get_json()
    filme_id = dados.get('filme_id')

    
    
    usuario_id = current_user.id
    if not usuario_id:
        abort(401, description="O usuário deve estar autenticado")

    if not filme_id:
        abort(400, description="É necessário informar filme_id")

    usuario = UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        abort(404, description="Usuário não encontrado.")

    filme = FilmeRepository.buscar_por_id(filme_id)
    if not filme:
        abort(404, description="Filme não encontrado.")

    aluguel = AluguelFactory.criar_aluguel(usuario_id=usuario.id, filme_id=filme.id)
    db.session.add(aluguel)
    db.session.commit()

    return jsonify({'mensagem': f'Filme "{filme.nome}" alugado com sucesso', 'aluguel_id': aluguel.id}), 200


@aluguel_bp.route('/meus-alugueis/avaliar/<int:aluguel_id>', methods=['POST']) # id do filme, pq ja tenho id do usuario
@login_required
def avaliar_filme_alugado(aluguel_id):
    """
    Avalia filme alugado por um usuário
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
      401:
        description: Usuário não autenticado
      403:
        description: Permissão inválida para avaliar o aluguel
      404:
        description: Aluguel não encontrado
    """
    dados = request.get_json()
    nota = dados.get('nota')

    
    usuario_id = current_user.id
    if not usuario_id:
        abort(401, description="O usuário deve estar autenticado")

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

    return jsonify({'mensagem': f'Nota {nota} registrada para o aluguel {aluguel.id} e filme ({filme.nome} / {filme.id}) atualizado.'}), 200




@aluguel_bp.route('/meus-alugueis', methods=['GET'])
@login_required
def lista_alugueis_usuario():
    """
    Lista filmes alugados do usuário
    ---
    responses:
      200:
        description: Lista de alugueis
      401:
        description: Usuário não autenticado
      404:
        description: Usuário não encontrado
    """
    

    usuario_id = current_user.id
    if not usuario_id:
        abort(401, description="O usuário deve estar autenticado")

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


#from app.models.aluguel import Aluguel
#@aluguel_bp.route('/meus-alugueis/avaliar/<int:aluguel_id>', methods=['POST'])
#@login_required
#def avaliar_filme_alugado(aluguel_id):
#    """
#    Avalia ou re-avalia um filme já alugado pelo usuário.
#    Se o usuário já tinha avaliado esse mesmo filme em outro(s) aluguel(eis),
#    o **total_avaliacoes permanece igual** e o impacto no `nota_final`
#    corresponde à **média** entre a nota antiga e a nova.
#    ---
#    parameters:
#      - name: aluguel_id
#        in: path
#        required: true
#        type: integer
#        description: ID do aluguel a ser avaliado
#      - name: body
#        in: body
#        required: true
#        schema:
#          properties:
#            nota:
#              type: number
#              format: float
#              description: Nota entre 0 e 10
#    responses:
#      200: {description: Nota registrada}
#      400: {description: Nota inválida ou erro de permissão}
#      401: {description: Usuário não autenticado}
#      403: {description: Avaliação não permitida}
#      404: {description: Aluguel não encontrado}
#    """
#    dados = request.get_json()
#    nota  = dados.get("nota")
#
#    if nota is None or not (0 <= nota <= 10):
#        abort(400, "Nota inválida: deve estar entre 0 e 10.")
#
#    usuario_id = current_user.id          
#    aluguel    = AluguelRepository.buscar_por_id(aluguel_id)
#    if not aluguel:
#        abort(404, "Aluguel não encontrado.")
#
#    if aluguel.usuario_id != usuario_id:
#        abort(403, "Você não tem permissão para avaliar este aluguel.")
#
#    filme = aluguel.filme
#
#    if aluguel.nota is not None:
#   
#        soma = filme.nota_final * filme.total_avaliacoes
#        soma = soma - aluguel.nota + nota
#        filme.nota_final = soma / filme.total_avaliacoes
#        aluguel.nota     = nota
#        db.session.commit()
#        return jsonify(
#            {"mensagem": f"Nota do aluguel {aluguel_id} atualizada para {nota}."}
#        ), 200
#
#    nota_antiga = (
#        Aluguel.query.filter_by(
#            usuario_id=usuario_id, filme_id=filme.id
#        )
#        .filter(Aluguel.nota.isnot(None))
#        .with_entities(Aluguel.nota)
#        .first()
#    )
#    if nota_antiga:
#        # já existia outra avaliação desse usuário para o mesmo filme
#        antiga = nota_antiga[0]
#        nota_media = (antiga + nota) / 2
#
#        soma = filme.nota_final * filme.total_avaliacoes
#        
#        soma = soma - antiga + nota_media
#        filme.nota_final = soma / filme.total_avaliacoes
#    else:
#        filme.total_avaliacoes += 1
#        soma = filme.nota_final * (filme.total_avaliacoes - 1) + nota
#        filme.nota_final = soma / filme.total_avaliacoes
#
#    aluguel.nota = nota
#    db.session.commit()
#
#    return (
#        jsonify(
#            {
#                "mensagem": (
#                    f"Nota {nota} registrada para o aluguel {aluguel_id}. "
#                    f"Filme {filme.nome} atualizado: "
#                    f"nota_final={filme.nota_final:.2f}, "
#                    f"total_avaliacoes={filme.total_avaliacoes}"
#                )
#            }
#        ),
#        200,
#    )
