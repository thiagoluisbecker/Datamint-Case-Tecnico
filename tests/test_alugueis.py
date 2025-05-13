from app.models.filme import Filme
from app.models.usuario import Usuario
from app import db



def test_alugar_filme(client, app):
    with app.app_context():
        usuario = Usuario(nome='Thiago', email='thiago@teste.com')
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add_all([usuario, filme])
        db.session.commit()

    response = client.post('/alugueis/', json={'usuario_id': 1, 'filme_id': 1})
    assert response.status_code == 201
    assert 'aluguel_id' in response.get_json()


def test_alugar_filme_usuario_inexistente(client):
    response = client.post('/alugueis/', json={'usuario_id': 99, 'filme_id': 1})
    assert response.status_code == 404


def test_avaliar_filme_alugado(client, app):
    with app.app_context():
        usuario = Usuario(nome='Thiago', email='thiago@teste.com')
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add_all([usuario, filme])
        db.session.commit()

        response = client.post('/alugueis/', json={'usuario_id': 1, 'filme_id': 1})
        aluguel_id = response.get_json()['aluguel_id']

    response = client.post(f'/alugueis/{aluguel_id}/avaliar', json={'nota': 8})
    assert response.status_code == 200


def test_avaliar_filme_com_nota_invalida(client, app):
    with app.app_context():
        usuario = Usuario(nome='Thiago', email='thiago@teste.com')
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add_all([usuario, filme])
        db.session.commit()

        response = client.post('/alugueis/', json={'usuario_id': 1, 'filme_id': 1})
        aluguel_id = response.get_json()['aluguel_id']

    response = client.post(f'/alugueis/{aluguel_id}/avaliar', json={'nota': 15})
    assert response.status_code == 400


def test_listar_alugueis_do_usuario(client, app):
    with app.app_context():
        usuario = Usuario(nome='Thiago', email='thiago@teste.com')
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add_all([usuario, filme])
        db.session.commit()

        client.post('/alugueis/', json={'usuario_id': 1, 'filme_id': 1})

    response = client.get('/alugueis/usuario/1/')
    assert response.status_code == 200
    assert b'Matrix' in response.data
