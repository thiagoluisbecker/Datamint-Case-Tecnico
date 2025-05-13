from app.models.aluguel import Aluguel
from datetime import datetime, timezone

class AluguelFactory:
    @staticmethod
    def criar_aluguel(usuario_id, filme_id, nota=None, data_locacao=None):
        if not data_locacao:
            data_locacao = datetime.now(timezone.utc)
        return Aluguel(
            usuario_id=usuario_id,
            filme_id=filme_id,
            data_locacao=data_locacao,
            nota=nota
        )
