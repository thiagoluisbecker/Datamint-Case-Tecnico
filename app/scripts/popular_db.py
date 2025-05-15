from app import create_app
from app.extensions import db
from app.models.aluguel import Aluguel
from app.repositories.filme_repository import FilmeRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.genero_repository import GeneroRepository
from app.factories.filme_factory import FilmeFactory
from app.factories.usuario_factory import UsuarioFactory
from app.factories.aluguel_factory import AluguelFactory
from app.factories.genero_factory import GeneroFactory
from datetime import datetime, timezone, timedelta
import random
from faker import Faker


fake = Faker('pt_BR')


def limpar_banco():
    """Limpa as tabelas do banco."""
    Aluguel.query.delete()
    db.session.commit()
    FilmeRepository.limpar_todos()
    UsuarioRepository.limpar_todos()
    GeneroRepository.limpar_todos()
    db.session.commit()


def criar_generos():
    """Cria generos fixos no banco."""
    nomes_generos = ['Ação', 'Drama', 'Comédia', 'Terror', 'Ficção Científica', 'Romance', 'Suspense']
    generos = [GeneroFactory.criar_genero(nome) for nome in nomes_generos]
    db.session.add_all(generos)
    db.session.commit()
    return generos


def criar_filmes(generos, quantidade=20):
    """Cria filmes associando a um genero_id existente."""
    filmes = [
        FilmeFactory.criar_filme(
            nome=fake.sentence(nb_words=3),
            genero_id=random.choice(generos).id,
            ano=random.randint(1950, 2024),
            sinopse=fake.text(max_nb_chars=150),
            diretor=fake.name()
        )
        for _ in range(quantidade)
    ]
    db.session.add_all(filmes)
    db.session.commit()
    return filmes


def criar_usuarios(quantidade=10):
    """Cria usuários com Factory e salva pelo Repository."""
    usuarios = [
        UsuarioFactory.criar_usuario(
            nome=fake.name(),
            celular=fake.phone_number(),
            email=fake.unique.email(),
            senha=f'teste{_}'
        )
        for _ in range(quantidade)
    ]
    
    db.session.add_all(usuarios)
    db.session.commit()
    return usuarios


def criar_alugueis(usuarios, filmes):
    """Cria alugueis variando usuários e filmes."""
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
        generos = criar_generos()
        filmes = criar_filmes(generos)
        usuarios = criar_usuarios()
        alugueis = criar_alugueis(usuarios, filmes)
        
        usuario_teste = UsuarioFactory.criar_usuario(
            nome='Thiago Rocha',
            celular=fake.phone_number(),
            email='thiagobeckerrocha@gmail.com',
            senha=f'teste_thiago'
        )
        db.session.add(usuario_teste)
        db.session.commit()
        

if __name__ == "__main__":
    popular_db()
