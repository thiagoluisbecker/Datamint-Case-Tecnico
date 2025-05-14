from app.factories.filme_factory import FilmeFactory
from app.models.usuario import Usuario
from app.factories.usuario_factory import UsuarioFactory
from app.factories.genero_factory import GeneroFactory
from app import db



def test_alugar_filme(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero('Ação')
        db.session.add(genero)
        db.session.commit()

        usuario = UsuarioFactory.criar_usuario(nome='Thiago', email='thiago@teste.com', celular = '1111111111111')
        filme = FilmeFactory.criar_filme('Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='...')

        db.session.add_all([usuario, filme])
        db.session.commit()

    response = client.post('/alugueis/', json={'filme_id': 1}, headers={'X-User-Id': 1})
    assert response.status_code == 200
    assert 'aluguel_id' in response.get_json()


def test_alugar_filme_usuario_inexistente(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero('Ação')
        db.session.add(genero)
        db.session.commit()

        filme = FilmeFactory.criar_filme('Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='...')
        db.session.add(filme)
        db.session.commit()

    response = client.post('/alugueis/', json={'filme_id': 1}, headers={'X-User-Id': 9999})
    assert response.status_code == 404



def test_avaliar_filme_alugado(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero('Ação')
        db.session.add(genero)
        db.session.commit()

        usuario = UsuarioFactory.criar_usuario(nome='Thiago', email='thiago@teste.com', celular = '1111111111111')
        filme = FilmeFactory.criar_filme('Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='...')
        db.session.add_all([usuario, filme])
        db.session.commit()

        response = client.post('/alugueis/', json={'filme_id': 1}, headers={'X-User-Id': 1})
        aluguel_id = response.get_json()['aluguel_id']

    response = client.post(f'/alugueis/meus-alugueis/avaliar/{aluguel_id}', json={'nota': 8}, headers={'X-User-Id': 1})
    
    assert response.status_code == 200


def test_avaliar_filme_que_usuario_nao_aluguou(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero('Ação')
        db.session.add(genero)
        db.session.commit()

        usuario1 = UsuarioFactory.criar_usuario(nome='Thiago', email='thiago@teste.com', celular = '1111111111111')
        usuario2 = UsuarioFactory.criar_usuario(nome='Outro User', email='outro@teste.com', celular = '1111111111111')
        filme = FilmeFactory.criar_filme('Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='...')
        db.session.add_all([usuario1, usuario2, filme])
        db.session.commit()

        response = client.post('/alugueis/', json={'filme_id': 1}, headers={'X-User-Id': 1})
        aluguel_id = response.get_json()['aluguel_id']

    response = client.post(f'/alugueis/meus-alugueis/avaliar/{aluguel_id}', json={'nota': 8}, headers={'X-User-Id': 2})
    assert response.status_code == 403


def test_avaliar_filme_com_nota_invalida(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero('Ação')
        db.session.add(genero)
        db.session.commit()

        usuario = UsuarioFactory.criar_usuario(nome='Thiago', email='thiago@teste.com', celular = '1111111111111')
        filme = FilmeFactory.criar_filme('Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='...')
        db.session.add_all([usuario, filme])
        db.session.commit()

        response = client.post('/alugueis/', json={'filme_id': 1}, headers={'X-User-Id': 1})
        aluguel_id = response.get_json()['aluguel_id']

    response = client.post(f'/alugueis/meus-alugueis/avaliar/{aluguel_id}', json={'nota': 15}, headers={'X-User-Id': 1})
    assert response.status_code == 400


def test_listar_meus_alugueis(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero('Ação')
        db.session.add(genero)
        db.session.commit()

        usuario = UsuarioFactory.criar_usuario(nome='Thiago', email='thiago@teste.com', celular='11111111111')
        db.session.add(usuario)
        db.session.commit()
        usuario_id = usuario.id  

        filme = FilmeFactory.criar_filme('Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='...')
        db.session.add(filme)
        db.session.commit()

        client.post('/alugueis/', json={'filme_id': filme.id}, headers={'X-User-Id': usuario.id  })

    response = client.get('/alugueis/meus-alugueis', headers={'X-User-Id': usuario_id})
    assert response.status_code == 200
    assert b'Matrix' in response.data



