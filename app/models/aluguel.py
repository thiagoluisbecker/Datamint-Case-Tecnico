from app import db



class Aluguel(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=False)
    data_locacao = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    nota = db.Column(db.Float)

    usuario = db.relationship('Usuario', back_populates='alugueis')
    filme = db.relationship('Filme', back_populates='alugueis')

    def __repr__(self):
         return f'{self.usuario.nome} Alugou {self.filme.nome}>'