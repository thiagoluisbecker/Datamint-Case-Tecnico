from app import db
from app.models.usuario import Usuario
from app.models.filme import Filme

def test_alugar_filme(app):
    with app.app_context():
        usuario = Usuario(nome='Teste', email='teste@teste.com')
        filme = Filme(nome='Matrix', genero='Ação', ano=1999)
        db.session.add_all([usuario, filme])
        db.session.commit()

    response = app.test_client().post('/alugueis/', json={'usuario_id': 1, 'filme_id': 1})
    assert response.status_code == 201
    assert 'aluguel_id' in response.get_json()
