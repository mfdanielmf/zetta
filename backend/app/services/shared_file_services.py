from uuid import UUID

from sqlalchemy.orm import Session

from app.models.archivo_compartido import ArchivoCompartido
from app.models import exceptions as ex
from app.models.file import File
from app.models.user import User
from app.schemas import shared_file_schemas as sfs
from app.schemas.file_schemas import FileBase
from app.services import user_services
from app.services import file_services
from app.repositories import shared_file_repo


def compartir_archivo(req: sfs.ShareFileRequest, usuario: User, db: Session) -> ArchivoCompartido:
    """
    UsuarioNoEncontradoException, ArchivoNoEncontradoException, PropietarioException, YaCompartidoException
    """
    if (req.correo_usuario).lower() == (usuario.correo).lower():
        raise ex.PropietarioException("Ya eres el propietario del archivo")

    # Comprobar si el receptor existe
    receptor: User = user_services.obtener_usuario_correo(
        correo=req.correo_usuario, db=db)

    if shared_file_repo.get_shared_file(id_archivo=req.id_archivo, id_receptor=receptor.id, db=db):
        raise ex.YaCompartidoException(
            f"Ya has compartido el archivo con {receptor.nombre}")

    # Archivo existe y el usuario es el dueño
    archivo: File = file_services.obtener_archivo_id(
        id=req.id_archivo, usuario=usuario, db=db)

    archivo_compartido: ArchivoCompartido = ArchivoCompartido(
        receptor=receptor, propietario=usuario, archivo=archivo)

    archivo_compartido_db = shared_file_repo.add_shared_file_db(
        archivo_compartido=archivo_compartido, db=db)

    return archivo_compartido_db


def obtener_archivos_compartidos(usuario: User, db: Session) -> list[sfs.ArchivoCompartidoBase]:
    archivos_compartidos: list[ArchivoCompartido] = shared_file_repo.get_all_shared_files_raiz(
        id_usuario=usuario.id, db=db)

    compartidos_base: list[sfs.ArchivoCompartidoBase] = []

    for a in archivos_compartidos:
        archivo_base: FileBase = FileBase(
            id=a.archivo.id,
            nombre_original=a.archivo.nombre_original,
            path=a.archivo.path,
            tamaño_bytes=a.archivo.tamaño_bytes,
            fecha_creacion=a.archivo.fecha_creacion,
            id_usuario=a.archivo.id_usuario,
            nombre_usuario=a.archivo.usuario.nombre,
            id_carpeta=a.archivo.id_carpeta,
            fecha_eliminacion=a.archivo.fecha_eliminacion
        )

        compartidos_base.append(
            sfs.ArchivoCompartidoBase(
                id=a.id,
                fecha_compartido=a.fecha_compartido,
                propietario=a.propietario,
                receptor=a.receptor,
                archivo=archivo_base
            )
        )

    return compartidos_base


def obtener_archivos_recibidos(usuario: User, db: Session) -> list[sfs.ArchivoCompartidoBase]:
    archivos_recibidos: list[ArchivoCompartido] = shared_file_repo.get_all_received_files_raiz(
        id_usuario=usuario.id, db=db)

    recibidos_base: list[sfs.ArchivoCompartidoBase] = []

    for a in archivos_recibidos:
        archivo_base: FileBase = FileBase(
            id=a.archivo.id,
            nombre_original=a.archivo.nombre_original,
            path=a.archivo.path,
            tamaño_bytes=a.archivo.tamaño_bytes,
            fecha_creacion=a.archivo.fecha_creacion,
            id_usuario=a.archivo.id_usuario,
            nombre_usuario=a.archivo.usuario.nombre,
            id_carpeta=a.archivo.id_carpeta,
            fecha_eliminacion=a.archivo.fecha_eliminacion
        )

        recibidos_base.append(
            sfs.ArchivoCompartidoBase(
                id=a.id,
                fecha_compartido=a.fecha_compartido,
                propietario=a.propietario,
                receptor=a.receptor,
                archivo=archivo_base
            )
        )

    return recibidos_base


def obtener_archivos_compartidos_paginados(usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[sfs.ArchivoCompartidoBase]]:
    offset: int = (pagina - 1) * limite

    total, archivos_compartidos = shared_file_repo.get_all_shared_files_raiz_paginados(
        id_usuario=usuario.id, db=db, offset=offset, limit=limite)

    compartidos_base: list[sfs.ArchivoCompartidoBase] = []

    for a in archivos_compartidos:
        archivo_base: FileBase = FileBase(
            id=a.archivo.id,
            nombre_original=a.archivo.nombre_original,
            path=a.archivo.path,
            tamaño_bytes=a.archivo.tamaño_bytes,
            fecha_creacion=a.archivo.fecha_creacion,
            id_usuario=a.archivo.id_usuario,
            nombre_usuario=a.archivo.usuario.nombre,
            id_carpeta=a.archivo.id_carpeta,
            fecha_eliminacion=a.archivo.fecha_eliminacion
        )

        compartidos_base.append(
            sfs.ArchivoCompartidoBase(
                id=a.id,
                fecha_compartido=a.fecha_compartido,
                propietario=a.propietario,
                receptor=a.receptor,
                archivo=archivo_base
            )
        )

    return total, compartidos_base


def obtener_archivos_recibidos_paginados(usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[sfs.ArchivoCompartidoBase]]:
    offset: int = (pagina - 1) * limite

    total, archivos_recibidos = shared_file_repo.get_all_received_files_raiz_paginados(
        id_usuario=usuario.id, db=db, offset=offset, limit=limite)

    recibidos_base: list[sfs.ArchivoCompartidoBase] = []

    for a in archivos_recibidos:
        archivo_base: FileBase = FileBase(
            id=a.archivo.id,
            nombre_original=a.archivo.nombre_original,
            path=a.archivo.path,
            tamaño_bytes=a.archivo.tamaño_bytes,
            fecha_creacion=a.archivo.fecha_creacion,
            id_usuario=a.archivo.id_usuario,
            nombre_usuario=a.archivo.usuario.nombre,
            id_carpeta=a.archivo.id_carpeta,
            fecha_eliminacion=a.archivo.fecha_eliminacion
        )

        recibidos_base.append(
            sfs.ArchivoCompartidoBase(
                id=a.id,
                fecha_compartido=a.fecha_compartido,
                propietario=a.propietario,
                receptor=a.receptor,
                archivo=archivo_base
            )
        )

    return total, recibidos_base


def obtener_archivo_compartido_no_receptor(id_compartido: UUID, id_propietario: UUID, db: Session) -> ArchivoCompartido:
    """
    ArchivoNoEncontradoException
    """

    archivo: ArchivoCompartido | None = shared_file_repo.get_shared_file_no_receptor(
        id_compartido=id_compartido, id_propietario=id_propietario, db=db)

    if not archivo:
        raise ex.ArchivoNoEncontradoException(
            f"No se ha encontrado el elemento compartido con ID {id_compartido}")

    return archivo
