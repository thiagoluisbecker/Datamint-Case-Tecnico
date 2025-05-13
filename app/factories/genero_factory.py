from app.models.genero import Genero

class GeneroFactory:
    @staticmethod
    def criar_genero(nome):
        return Genero(nome=nome)
