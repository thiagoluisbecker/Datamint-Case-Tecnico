from app.factories.filme_factory import FilmeFactory
from app.factories.genero_factory import GeneroFactory
from app import db


#---TEstes filmes_por_genero ---
def test_get_filmes_por_genero_com_filmes(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero(nome='Ação')
        db.session.add(genero)
        db.session.commit()

        filme1 = FilmeFactory.criar_filme(nome='Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='Wachowski')
        filme2 = FilmeFactory.criar_filme(nome='Mad Max', genero_id=genero.id, ano=1979, sinopse='...', diretor='George Miller')
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
        genero = GeneroFactory.criar_genero(nome='Comédia')
        db.session.add(genero)
        db.session.commit()

  
        response = client.get(f'/filmes/genero/{genero.id}')
        assert response.status_code == 404

        data = response.get_json()
        assert 'mensagem' in data
        assert data['mensagem'] == f'Nenhum filme encontrado para o gênero ID: {genero.id}'



#---TEstes detalhes_filme ---
def test_detalhes_filme_nao_existente(client):
    response = client.get('/filmes/1')
    assert response.status_code == 404


def test_detalhes_filme_existente(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero(nome='Ação')
        db.session.add(genero)
        db.session.commit()

        filme = FilmeFactory.criar_filme(nome='Matrix', genero_id=genero.id, ano=1999, sinopse='...', diretor='Wachowski')
        db.session.add(filme)
        db.session.commit()

    response = client.get('/filmes/1')
    assert response.status_code == 200
    assert b'Matrix' in response.data



