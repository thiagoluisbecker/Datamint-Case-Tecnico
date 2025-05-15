from app.models.aluguel import Aluguel
from app.extensions import db

class AluguelRepository:
    
    @staticmethod
    def listar_por_usuario(usuario_id):
        return Aluguel.query.filter_by(usuario_id=usuario_id).all()
    
    @staticmethod
    def buscar_por_id(aluguel_id):
        return Aluguel.query.get(aluguel_id)

