from app import create_app, db
from app.repositories.filme_repository import FilmeRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.factories.filme_factory import FilmeFactory
from app.factories.usuario_factory import UsuarioFactory
from app.factories.aluguel_factory import AluguelFactory
from app.models.aluguel import Aluguel
from datetime import datetime, timezone, timedelta
import random
from faker import Faker

fake = Faker('pt_BR')


def limpar_banco():
    Aluguel.query.delete()
    db.session.commit()
    FilmeRepository.limpar_todos()
    UsuarioRepository.limpar_todos()
    db.session.commit()


def criar_filmes(quantidade=100):
    generos = ['Ação', 'Drama', 'Comédia', 'Terror', 'Ficção Científica', 'Romance', 'Suspense']
    filmes = [
        FilmeFactory.criar_filme(
            nome=fake.sentence(nb_words=3),
            genero=random.choice(generos),
            ano=random.randint(1950, 2024),
            sinopse=fake.text(max_nb_chars=150),
            diretor=fake.name()
        )
        for _ in range(quantidade)
    ]
    db.session.add_all(filmes)
    db.session.commit()
    return filmes


def criar_usuarios(quantidade=50):
    usuarios = [
        UsuarioFactory.criar_usuario(
            nome=fake.name(),
            celular=fake.phone_number(),
            email=fake.unique.email()
        )
        for _ in range(quantidade)
    ]
    db.session.add_all(usuarios)
    db.session.commit()
    return usuarios


def criar_alugueis(usuarios, filmes):
    alugueis = []
    usuarios_com_alugueis = random.sample(usuarios, int(len(usuarios) * 0.7))
    filmes_possiveis_para_alugar = random.sample(filmes, int(len(filmes) * 0.6))

    for usuario in usuarios_com_alugueis:
        filmes_aleatorios = random.sample(filmes_possiveis_para_alugar, random.randint(1, 5))
        for filme in filmes_aleatorios:
            aluguel = AluguelFactory.criar_aluguel(
                usuario_id=usuario.id,
                filme_id=filme.id,
                data_locacao=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 365)),
                nota=random.choice([None, 3.0, 4.0, 4.5, 5.0])
            )
            alugueis.append(aluguel)
    db.session.add_all(alugueis)
    db.session.commit()
    return alugueis


def popular_db():
    app = create_app()
    with app.app_context():
        limpar_banco()
        filmes = criar_filmes()
        usuarios = criar_usuarios()
        criar_alugueis(usuarios, filmes)
        
if __name__ == "__main__":
    popular_db()
