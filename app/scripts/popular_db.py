from app import create_app, db
from app.models.filme import Filme
from app.models.usuario import Usuario
from app.models.aluguel import Aluguel
from datetime import datetime, timezone
import random

# python -m app.scripts.popular_db

def popular_db():
    app = create_app()

    filmes = []
    with app.app_context():
        # Limpar dados
        Aluguel.query.delete()
        Filme.query.delete()
        Usuario.query.delete()
        db.session.commit()

        # Criar filmes
        filmes = [
            Filme(nome='O Poderoso Chefão', genero='Drama', ano=1972, sinopse='Mafia em NY', diretor='Francis Ford Coppola'),
            Filme(nome='Pulp Fiction', genero='Crime', ano=1994, sinopse='Histórias interligadas', diretor='Quentin Tarantino'),
            Filme(nome='Matrix', genero='Ficção Científica', ano=1999, sinopse='Realidade virtual', diretor='Lana Wachowski, Lilly Wachowski'),
        ]
        db.session.add_all(filmes)

        # Criar usuários
        usuarios = [
            Usuario(nome='João Silva', celular='21999999999', email='joao@example.com'),
            Usuario(nome='Maria Souza', celular='21988888888', email='maria@example.com'),
        ]
        db.session.add_all(usuarios)

        db.session.commit()

        # Criar alugueis aleatorios
        alugueis = []
        for usuario in usuarios:
            for filme in random.sample(filmes, 2):
                alugueis.append(
                    Aluguel(usuario_id=usuario.id, filme_id=filme.id, data_locacao=datetime.now(timezone.utc), nota=random.choice([3.0, 4.5, 5.0]))
                )
        db.session.add_all(alugueis)
        db.session.commit()
    
if __name__=="__main__":
    popular_db() 