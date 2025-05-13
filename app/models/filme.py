from app import db

class Filme(db.Model):
    __tablename__ = 'filmes'

    id = db.Column(db.Integer, primary_key = True)
    genero_id = db.Column(db.Integer, db.ForeignKey('generos.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    sinopse = db.Column(db.Text)
    diretor = db.Column(db.String(100))
    
    genero = db.relationship('Genero', back_populates='filmes')
    alugueis = db.relationship('Aluguel', back_populates='filme')

    def __repr__(self):
         return f'{self.nome}'