from app.models.filme import Filme

class FilmeFactory:
    @staticmethod
    def criar_filme(nome, genero, ano, sinopse, diretor):
        return Filme(
            nome=nome,
            genero=genero,
            ano=ano,
            sinopse=sinopse,
            diretor=diretor
        )
