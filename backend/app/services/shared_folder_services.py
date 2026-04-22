from sqlalchemy.orm import Session

from app.models.carpeta_compartida import CarpetaCompartida
from app.models.exceptions import PropietarioException, YaCompartidoException
from app.models.folder import Folder
from app.models.user import User
from app.repositories import shared_folder_repo
from app.schemas import shared_folder_schemas as sfs
from app.services import folder_services, user_services


def compartir_carpeta(req: sfs.ShareFolderRequest, usuario: User, db: Session) -> CarpetaCompartida:
    """
    PropietarioException, CarpetaNoEncontradaException, YaCompartidoException, UsuarioNoEncontradoException
    """
    if (req.correo_usuario).lower() == (usuario.correo).lower():
        raise PropietarioException("Ya eres el propietario de la carpeta")

    receptor: User = user_services.obtener_usuario_correo(
        correo=req.correo_usuario, db=db)

    if shared_folder_repo.get_shared_folder(id_carpeta=req.id_carpeta, id_receptor=receptor.id, db=db):
        raise YaCompartidoException(
            f"Ya has compartido la carpeta con {receptor.nombre}")

    carpeta: Folder = folder_services.obtener_carpeta_usuario_id(
        id_carpeta=req.id_carpeta, usuario=usuario, db=db)

    carpeta_compartida: CarpetaCompartida = CarpetaCompartida(
        propietario=usuario, receptor=receptor, carpeta=carpeta)

    carpeta_compartida_db: CarpetaCompartida = shared_folder_repo.add_shared_folder_db(
        carpeta_compartida=carpeta_compartida, db=db)

    return carpeta_compartida_db
