from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

class UsuarioFactory:
    
    @staticmethod
    def criar_usuario(nome, celular, email, senha):
        return Usuario(
            nome=nome,
            celular=celular,
            email=email,
            senha = generate_password_hash(senha),
        )