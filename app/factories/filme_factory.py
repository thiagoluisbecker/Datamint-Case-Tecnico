from app.models.filme import Filme

class FilmeFactory:
    @staticmethod
    def criar_filme(nome, genero=None, genero_id=None, **kwargs):
        if not genero and genero_id is None:
            raise ValueError("Informe genero ou genero_id")
        filme = Filme(
            nome=nome,
            genero=genero,              
            genero_id=genero_id,        
            **kwargs
        )
        return filme