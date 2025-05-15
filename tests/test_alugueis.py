from app.factories.filme_factory import FilmeFactory
from app.factories.usuario_factory import UsuarioFactory
from app.factories.genero_factory import GeneroFactory
from werkzeug.security import generate_password_hash
from app.extensions import db

def login(client, email, senha):
    return client.post("/auth/login", json={"email": email, "senha": senha})



#--- TEstes alugar_filme ---

def test_alugar_filme(client, app):
    with app.app_context():
        genero  = GeneroFactory.criar_genero("Ação")
        usuario = UsuarioFactory.criar_usuario(
            nome="Thiago",
            email="thiago@teste.com",
            celular="11111111111",
            senha="teste"     
        )
        filme   = FilmeFactory.criar_filme(
            "Matrix", genero=genero, ano=1999, sinopse="...", diretor="..."
        )
        db.session.add_all([genero, usuario, filme])
        db.session.commit()

   
        resp_login = login(client, usuario.email, "teste")
        assert resp_login.status_code == 200

        resp = client.post("/alugueis/", json={"filme_id": filme.id})
        assert resp.status_code == 200
        assert "aluguel_id" in resp.get_json()


def test_alugar_filme_usuario_inexistente(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero("Ação")
        filme  = FilmeFactory.criar_filme("Matrix", genero=genero, ano=1999)
        db.session.add_all([genero, filme]); db.session.commit()


        resp = client.post("/alugueis/", json={"filme_id": filme.id})
        assert resp.status_code == 401

def test_alugar_filme_filme_inexistente(client, app):
    with app.app_context():
        usuario = UsuarioFactory.criar_usuario(
            nome="Thiago",
            email="thiago@teste.com",
            celular="11111111111",
            senha="teste"     
        )
        db.session.add(usuario); db.session.commit()

        login(client, usuario.email, "teste")         

        resp = client.post("/alugueis/", json={"filme_id": 999})
        assert resp.status_code == 404           



#--- Testes avaliar_filme ---
def test_avaliar_filme_alugado(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero("Ação")
        usuario = UsuarioFactory.criar_usuario(
            nome="Thiago",
            email="thiago@teste.com",
            celular="11111111111",
            senha="teste"      
        )
        filme = FilmeFactory.criar_filme(
            "Matrix",
            genero=genero,
            ano=1999,
            sinopse="...",
            diretor="..."
        )
        db.session.add_all([genero, usuario, filme])
        db.session.commit()

        assert login(client, usuario.email, "teste").status_code == 200

        resp_alugar = client.post("/alugueis/", json={"filme_id": filme.id})
        assert resp_alugar.status_code == 200         
        data = resp_alugar.get_json()
        assert "aluguel_id" in data                   
        aluguel_id = data["aluguel_id"]

        resp_avaliar = client.post(
            f"/alugueis/meus-alugueis/avaliar/{aluguel_id}",   
            json={"nota": 8}
        )
        assert resp_avaliar.status_code == 200


def test_avaliar_filme_que_usuario_nao_aluguou(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero("Ação")

        usuario1 = UsuarioFactory.criar_usuario(
            nome="Thiago",
            email="thiago@teste.com",
            celular="11111",
            senha="teste"
        )
        usuario2 = UsuarioFactory.criar_usuario(
            nome="Outro",
            email="outro@teste.com",
            celular="22222",
            senha="teste2"
        )

        filme = FilmeFactory.criar_filme(
            "Matrix",
            genero=genero,
            ano=1999,
            sinopse="...",
            diretor="..."
        )
        db.session.add_all([genero, usuario1, usuario2, filme])
        db.session.commit()

        assert login(client, usuario1.email, "teste").status_code == 200

        resp_alugar = client.post("/alugueis/", json={"filme_id": filme.id})
        assert resp_alugar.status_code == 200               
        aluguel_id = resp_alugar.get_json()["aluguel_id"]   

        
        client.post("/auth/logout")

        
        assert login(client, usuario2.email, "teste2").status_code == 200

        resp_avaliar = client.post(
            f"/alugueis/meus-alugueis/avaliar/{aluguel_id}",
            json={"nota": 8}
        )
        assert resp_avaliar.status_code == 403              


def test_avaliar_filme_com_nota_invalida(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero("Ação")

        usuario = UsuarioFactory.criar_usuario(
            nome="Thiago",
            email="thiago@teste.com",
            celular="11111111111",
            senha="teste"                 
        )
        filme = FilmeFactory.criar_filme(
            "Matrix",
            genero=genero,
            ano=1999,
            sinopse="...",
            diretor="..."
        )
        db.session.add_all([genero, usuario, filme])
        db.session.commit()

        login(client, usuario.email, "teste")

        resp_alugar = client.post("/alugueis/", json={"filme_id": filme.id})
        assert resp_alugar.status_code == 200          
        aluguel_id = resp_alugar.get_json()["aluguel_id"]
    
        resp_avaliar = client.post(
            f"/alugueis/meus-alugueis/avaliar/{aluguel_id}",
            json={"nota": 15}
        )
        assert resp_avaliar.status_code == 400          


#--- Testes listar_alugueis ---
def test_listar_meus_alugueis(client, app):
    with app.app_context():
        genero = GeneroFactory.criar_genero("Ação")
        usuario = UsuarioFactory.criar_usuario(
            nome="Thiago",
            email="thiago@teste.com",
            celular="11111111111",
            senha="teste"                     # texto → factory grava hash
        )
        filme = FilmeFactory.criar_filme(
            "Matrix",
            genero=genero,
            ano=1999,
            sinopse="...",
            diretor="..."
        )
        db.session.add_all([genero, usuario, filme])
        db.session.commit()

        login(client, usuario.email, "teste")

        resp_alugar = client.post("/alugueis/", json={"filme_id": filme.id})
        assert resp_alugar.status_code == 200
    
        resp_lista = client.get("/alugueis/meus-alugueis")
        assert resp_lista.status_code == 200
        assert b"Matrix" in resp_lista.data



