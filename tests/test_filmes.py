from app.models.filme import Filme
from app.models.genero import Genero
from app import db


#---TEstes detalhes_filme ---
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



#---TEstes filmes_por_genero ---
def test_get_filmes_por_genero_com_filmes(client, app):
    with app.app_context():
        genero = Genero(nome='Ação')
        db.session.add(genero)
        db.session.commit()

        filme1 = Filme(nome='Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='Wachowski')
        filme2 = Filme(nome='Mad Max', genero_id=genero.id, ano=1979, sinopse='...', diretor='George Miller')
        db.session.add_all([filme1, filme2])
        db.session.commit()

    
    response = client.get(f'/filmes/genero/{genero.id}')
    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2

    nomes = {f['nome'] for f in data}
    assert 'Matrix' in nomes
    assert 'Mad Max' in nomes

    
    for filme in data:
        assert 'id' in filme
        assert 'nome' in filme
        assert 'genero' in filme and filme['genero'] == 'Ação'
        assert 'sinopse' in filme
        assert 'diretor' in filme
        assert 'ano' in filme


def test_get_filmes_por_genero_sem_filmes(client, app):
    with app.app_context():
        genero = Genero(nome='Comédia')
        db.session.add(genero)
        db.session.commit()

  
    response = client.get(f'/filmes/genero/{genero.id}')
    assert response.status_code == 404

    data = response.get_json()
    assert 'mensagem' in data
    assert data['mensagem'] == f'Nenhum filme encontrado para o gênero ID: {genero.id}'