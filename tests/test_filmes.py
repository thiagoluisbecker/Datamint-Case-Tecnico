from app.models.filme import Filme
from app import db

def test_listar_filmes_vazio(client):
    response = client.get('/filmes/')
    assert response.status_code == 404


def test_listar_filmes_com_dados(client, app):
    with app.app_context():
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add(filme)
        db.session.commit()

    response = client.get('/filmes/')
    assert response.status_code == 200
    assert b'Matrix' in response.data


def test_detalhes_filme_nao_existente(client):
    response = client.get('/filmes/1')
    assert response.status_code == 404


def test_detalhes_filme_existente(client, app):
    with app.app_context():
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add(filme)
        db.session.commit()

    response = client.get('/filmes/1')
    assert response.status_code == 200
    assert b'Matrix' in response.data
