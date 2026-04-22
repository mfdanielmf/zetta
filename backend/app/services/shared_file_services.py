from sqlalchemy.orm import Session

from app.models.archivo_compartido import ArchivoCompartido
from app.models.exceptions import PropietarioException, YaCompartidoException
from app.models.file import File
from app.models.user import User
from app.schemas import shared_file_schemas as sfs
from app.services import user_services
from app.services import file_services
from app.repositories import shared_file_repo


def compartir_archivo(req: sfs.ShareFileRequest, usuario: User, db: Session) -> ArchivoCompartido:
    """
    UsuarioNoEncontradoException, ArchivoNoEncontradoException, PropietarioException, YaCompartidoException
    """
    if (req.correo_usuario).lower() == (usuario.correo).lower():
        raise PropietarioException("Ya eres el propietario del archivo")

    # Comprobar si el receptor existe
    receptor: User = user_services.obtener_usuario_correo(
        correo=req.correo_usuario, db=db)

    if shared_file_repo.get_shared_file(id_archivo=req.id_archivo, id_receptor=receptor.id, db=db):
        raise YaCompartidoException(
            f"Ya has compartido el archivo con {receptor.nombre}")

    # Archivo existe y el usuario es el dueño
    archivo: File = file_services.obtener_archivo_id(
        id=req.id_archivo, usuario=usuario, db=db)

    archivo_compartido: ArchivoCompartido = ArchivoCompartido(
        receptor=receptor, propietario=usuario, archivo=archivo)

    archivo_compartido_db = shared_file_repo.add_shared_file_db(
        archivo_compartido=archivo_compartido, db=db)

    return archivo_compartido_db
