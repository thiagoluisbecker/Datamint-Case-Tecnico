from app import create_app, db
from app.models import aluguel, filme, usuario

# python -m app.scripts.popular_db

def popular_db():
    app = create_app()

    with app.app_context():

        for i in range(5):
            novo_filme = filme.Filme(nome=f'Star Wars {i+1}', genero='Ficcao cientifica', diretor='George Lucas', ano=1980+i)    
            db.session.add(novo_filme)
        
        db.session.commit()

if __name__=="__main__":
    popular_db() 