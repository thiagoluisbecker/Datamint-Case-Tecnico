from app.models.filme import Filme
from app.models.genero import Genero
from app import db



def test_detalhes_filme_nao_existente(client):
    response = client.get('/filmes/1')
    assert response.status_code == 404


def test_detalhes_filme_existente(client, app):
    with app.app_context():
        genero = Genero(nome='Ação')
        db.session.add(genero)
        db.session.commit()

        filme = Filme(nome='Matrix', genero_id=genero.id, ano=1999)
        db.session.add(filme)
        db.session.commit()

    response = client.get('/filmes/1')
    assert response.status_code == 200
    assert b'Matrix' in response.data
