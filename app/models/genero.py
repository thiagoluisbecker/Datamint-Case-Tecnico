from app import db

class Genero(db.Model):
    __tablename__ = 'generos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    filmes = db.relationship('Filme', back_populates='genero')

    def __repr__(self):
        return f'{self.nome}'
