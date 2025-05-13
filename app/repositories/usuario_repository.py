from app.models.usuario import Usuario

class UsuarioRepository:
    
    def listar_todos():
        return Usuario.query.all()

   
    def buscar_por_id(usuario_id):
        return Usuario.query.get(usuario_id)