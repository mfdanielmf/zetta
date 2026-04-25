from sqlalchemy.orm import Session

from app.models.carpeta_compartida import CarpetaCompartida
from app.models.exceptions import PropietarioException, YaCompartidoException
from app.models.folder import Folder
from app.models.user import User
from app.repositories import shared_folder_repo
from app.schemas import shared_folder_schemas as sfs
from app.schemas.folder_schemas import FolderBase
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


def obtener_carpetas_compartidas(usuario: User, db: Session) -> list[sfs.CarpetaCompartidaBase]:
    carpetas_compartidas: list[CarpetaCompartida] = shared_folder_repo.get_all_shared_folders_raiz(
        id_usuario=usuario.id, db=db)

    compartidos_base: list[sfs.CarpetaCompartidaBase] = []

    for c in carpetas_compartidas:
        carpeta_base: FolderBase = FolderBase(
            id=c.carpeta.id,
            nombre_original=c.carpeta.nombre_original,
            path=c.carpeta.path,
            fecha_creacion=c.carpeta.fecha_creacion,
            id_usuario=c.carpeta.id_usuario,
            nombre_usuario=c.carpeta.usuario.nombre,
            id_carpeta=c.carpeta.id_carpeta,
            fecha_eliminacion=c.carpeta.fecha_eliminacion
        )

        compartidos_base.append(
            sfs.CarpetaCompartidaBase(
                id=c.id,
                fecha_compartido=c.fecha_compartido,
                propietario=c.propietario,
                receptor=c.receptor,
                carpeta=carpeta_base
            )
        )

    return compartidos_base
