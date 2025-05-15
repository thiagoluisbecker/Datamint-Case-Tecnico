from app.models.filme import Filme
from app.extensions import db

class FilmeRepository:

    @staticmethod
    def listar_todos():
        return Filme.query.all()
    
    @staticmethod
    def buscar_por_id( filme_id):
        return Filme.query.get_or_404(filme_id)
    
    @staticmethod
    def listar_por_genero_id(genero_id):
        return Filme.query.filter_by(genero_id=genero_id).all()

    @staticmethod
    def limpar_todos():
        Filme.query.delete()
        db.session.commit()

        