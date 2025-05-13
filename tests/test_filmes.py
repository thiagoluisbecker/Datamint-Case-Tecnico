def test_listar_filmes_vazio(app):
    response = app.test_client().get('/filmes/')
    assert response.status_code == 200
    assert response.get_json() == []

def test_detalhes_filme_nao_existente(app):
    response = app.test_client().get('/filmes/1')
    assert response.status_code == 404

