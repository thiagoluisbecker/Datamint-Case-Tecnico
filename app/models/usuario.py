from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    nome = db.Column(db.String(100), nullable = False)
    celular = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True) 
    