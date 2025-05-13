from app.models.filme import Filme

class FilmeFactory:
    @staticmethod
    def criar_filme(nome, genero_id, ano, sinopse, diretor):
        return Filme(
            nome=nome,
            genero_id=genero_id,
            ano=ano,
            sinopse=sinopse,
            diretor=diretor
        )
