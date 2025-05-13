from app.models.genero import Genero

class GeneroRepository:
    @staticmethod
    def listar_todos():
        return Genero.query.all()

    @staticmethod
    def buscar_por_id(genero_id):
        return Genero.query.get(genero_id)

    @staticmethod
    def limpar_todos():
        Genero.query.delete()
