from app.models.filme import Filme
from app import db

class FilmeRepository:

    @staticmethod
    def listar_todos():
        return Filme.query.all()
    
    @staticmethod
    def buscar_por_id( filme_id):
        return Filme.query.get_or_404(filme_id)
    
    @staticmethod
    def listar_por_genero(genero):
        return Filme.query.filter_by(genero=genero).all()

