from app.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    celular = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable = False, unique = True) 
    senha   = db.Column(db.String(128), nullable=False) 

    alugueis = db.relationship('Aluguel', back_populates='usuario')
    
    def __repr__(self):
         return f'{self.nome}'