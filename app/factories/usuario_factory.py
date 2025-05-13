from app.models.usuario import Usuario

class UsuarioFactory:
    
    @staticmethod
    def criar_usuario(nome, celular, email):
        return Usuario(
            nome=nome,
            celular=celular,
            email=email
        )