from app import db

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    nome = db.Column(db.String(100), nullable = False)
    genero = db.Column(db.String(100), nullable = False)
    ano = db.Column(db.String(100), nullable = False)
    sinopse = db.Column(db.String(15), nullable = False)
    diretor = db.Column(db.String(100), nullable = False) 
    