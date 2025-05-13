from app.models.filme import Filme
from app import db

class FilmeRepository:

    def listar_todos(self):
        return Filme.query.all()
    
    def buscar_por_id(self, filme_id):
        return Filme.query.get_or_404(filme_id)
    
    def listar_por_genero(genero):
        return Filme.query.filter_by(genero=genero).all()

