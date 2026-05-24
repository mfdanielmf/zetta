import os
import shutil
from datetime import datetime, timezone
import tempfile
import zipfile

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.archivo_compartido import ArchivoCompartido
from app.models.archivo_favorito import ArchivoFavorito
from app.models.carpeta_compartida import CarpetaCompartida
from app.models.carpeta_favorita import CarpetaFavorita
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.models import exceptions as ex
from app.services import file_services, folder_services, user_services, shared_file_services, shared_folder_services
from app.repositories import file_repo, folder_repo, multiple_repo, shared_file_repo, shared_folder_repo, favorite_repo
from app.schemas import multiple_schemas


def añadir_multiples_items_papelera(items: list[multiple_schemas.ItemMultipleRequest], usuario: User, db: Session):
    errores = []

    fecha_actual = datetime.now(timezone.utc)

    for item in items:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":

                if file_repo.get_file_trash(id_archivo=item.id, id_usuario=usuario.id, db=db):
                    raise ex.ArchivoPapeleraException(
                        "El archivo ya está en la papelera")

                archivo: File = file_services.obtener_archivo_id(
                    id=item.id, usuario=usuario, db=db)

                nombre_item = archivo.nombre_original or "desconocido"

                archivo.fecha_eliminacion = fecha_actual

                file_repo.update_file(archivo=archivo, db=db)

            else:
                if folder_repo.get_folder_trash(id_carpeta=item.id, id_usuario=usuario.id, db=db):
                    raise ex.CarpetaPapeleraException(
                        "La carpeta ya está en la papelera")

                carpeta: Folder = folder_services.obtener_carpeta_usuario_id(
                    id_carpeta=item.id, usuario=usuario, db=db)

                nombre_item = carpeta.nombre_original or "desconocida"

                path_padre = carpeta.path

                carpeta.fecha_eliminacion = fecha_actual

                db.query(Folder).filter(
                    Folder.id_usuario == usuario.id,
                    or_(
                        Folder.path == path_padre,
                        Folder.path.like(f"{path_padre}/%")
                    )
                ).update(
                    {Folder.fecha_eliminacion: fecha_actual},
                    synchronize_session=False
                )

                db.query(File).filter(
                    File.id_usuario == usuario.id,
                    File.path.like(f"{path_padre}/%")
                ).update(
                    {File.fecha_eliminacion: fecha_actual},
                    synchronize_session=False
                )

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores


def eliminar_multiples_items_permanente(items: list[multiple_schemas.ItemMultipleRequest], usuario: User, db: Session):
    errores = []

    for item in items:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":

                archivo: File = file_services.obtener_archivo_papelera(
                    id_archivo=item.id, usuario=usuario, db=db)

                nombre_item = archivo.nombre_original or "desconocido"

                if os.path.exists(archivo.path):
                    os.remove(archivo.path)

                multiple_repo.delete_file(archivo=archivo, db=db)

            else:
                carpeta: Folder = folder_services.obtener_carpeta_papelera(
                    id_carpeta=item.id, usuario=usuario, db=db)

                nombre_item = carpeta.nombre_original or "desconocida"

                if os.path.exists(carpeta.path):
                    shutil.rmtree(carpeta.path)

                multiple_repo.delete_folder(carpeta=carpeta, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores


def restaurar_multiples_items_papelera(items: list[multiple_schemas.ItemMultipleRequest], usuario: User, db: Session):
    errores = []

    for item in items:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":
                archivo: File = file_services.obtener_archivo_papelera(
                    id_archivo=item.id, db=db, usuario=usuario)

                nombre_item = archivo.nombre_original or "desconocido"

                archivo.fecha_eliminacion = None

                file_repo.update_file(archivo=archivo, db=db)

            else:
                carpeta: Folder = folder_services.obtener_carpeta_papelera(
                    id_carpeta=item.id, usuario=usuario, db=db)

                nombre_item = carpeta.nombre_original or "desconocida"

                path_padre: str = carpeta.path

                carpeta.fecha_eliminacion = None

                db.query(Folder).filter(
                    Folder.id_usuario == usuario.id,
                    or_(
                        Folder.path == path_padre,
                        Folder.path.like(f"{path_padre}/%")
                    )
                ).update(
                    {Folder.fecha_eliminacion: None},
                    synchronize_session=False
                )

                db.query(File).filter(
                    File.id_usuario == usuario.id,
                    File.path.like(f"{path_padre}/%")
                ).update(
                    {File.fecha_eliminacion: None},
                    synchronize_session=False
                )

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores


def compartir_multiples_items(req: multiple_schemas.ShareMultipleItemsRequest, usuario: User, db: Session):
    """
    UsuarioNoEncontradoException, PropietarioException
    """
    errores = []

    if req.correo_usuario.lower() == usuario.correo.lower():
        raise ex.PropietarioException(
            "Ya eres el propietario de los elementos")

    receptor: User = user_services.obtener_usuario_correo(
        correo=req.correo_usuario, db=db)

    for item in req.items:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":
                archivo: File = file_services.obtener_archivo_id(
                    id=item.id, usuario=usuario, db=db)

                nombre_item = archivo.nombre_original or "desconocido"

                if shared_file_repo.get_shared_file(id_archivo=item.id, id_receptor=receptor.id, db=db):
                    raise ex.YaCompartidoException(
                        f"Ya has compartido el archivo con {receptor.nombre}")

                archivo_compartido = ArchivoCompartido(
                    receptor=receptor, propietario=usuario, archivo=archivo)

                shared_file_repo.add_shared_file_db(
                    archivo_compartido=archivo_compartido, db=db)

            else:
                carpeta: Folder = folder_services.obtener_carpeta_usuario_id(
                    id_carpeta=item.id,
                    usuario=usuario,
                    db=db
                )

                nombre_item = carpeta.nombre_original or "desconocida"

                if shared_folder_repo.get_shared_folder(id_carpeta=item.id, id_receptor=receptor.id, db=db):
                    raise ex.YaCompartidoException(
                        f"Ya has compartido la carpeta con {receptor.nombre}")

                carpeta_compartida = CarpetaCompartida(
                    propietario=usuario, receptor=receptor, carpeta=carpeta)

                shared_folder_repo.add_shared_folder_db(
                    carpeta_compartida=carpeta_compartida, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    return errores


def descargar_multiples_items(items: list[multiple_schemas.ItemMultipleRequest], usuario: User, db: Session):
    """
    ArchivoNoEncontradoException, CarpetaNoEncontradaException
    """
    archivo_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    zip_path: str = archivo_temp.name
    archivo_temp.close()

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

            for item in items:
                if item.tipo == "archivo":
                    archivo: File = file_services.obtener_archivo_permisos(
                        id_archivo=item.id, usuario=usuario, db=db)

                    if os.path.exists(archivo.path):
                        zipf.write(
                            archivo.path, arcname=archivo.nombre_original)

                else:
                    carpeta: Folder = folder_services.obtener_carpeta_usuario_permisos(
                        id_carpeta=item.id, usuario=usuario, db=db)

                    folder_services.añadir_carpeta_a_zip(
                        zipf=zipf, carpeta=carpeta, path_base="")

        return zip_path
    except Exception:
        if os.path.exists(zip_path):
            os.remove(zip_path)

            raise


def cancelar_multiples_compartidos(req: list[multiple_schemas.ItemMultipleRequest], usuario: User, db: Session):
    """
    UsuarioNoEncontradoException
    """
    errores = []

    for item in req:
        nombre_item = "desconocido"

        try:
            if not item.id_compartido:
                raise Exception("Falta id_compartido")

            if item.tipo == "archivo":
                archivo_compartido: ArchivoCompartido = shared_file_services.obtener_archivo_compartido_no_receptor(
                    id_compartido=item.id_compartido, id_propietario=usuario.id, db=db)

                if not archivo_compartido:
                    raise ex.ArchivoNoEncontradoException(
                        "No se ha encontrado el archivo compartido")

                nombre_item = archivo_compartido.archivo.nombre_original or "desconocido"

                db.delete(archivo_compartido)

            else:
                carpeta_compartida: CarpetaCompartida = shared_folder_services.obtener_carpeta_compartida_no_receptor(
                    id_compartido=item.id_compartido, id_propietario=usuario.id, db=db)

                if not carpeta_compartida:
                    raise ex.CarpetaNoEncontradaException(
                        "No se ha encontrado la carpeta compartida")

                nombre_item = carpeta_compartida.carpeta.nombre_original or "desconocido"

                db.delete(carpeta_compartida)

        except Exception as e1:
            errores.append({
                "id_item": str(item.id_compartido),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores


def toggle_multiples_favoritos(req: list[multiple_schemas.ItemMultipleRequest], usuario: User, db: Session):
    errores = []

    for item in req:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":
                archivo: File = file_services.obtener_archivo_permisos(
                    id_archivo=item.id, usuario=usuario, db=db)

                favorito: ArchivoFavorito | None = favorite_repo.get_favorite_file_user_by_file_id(
                    id_archivo=archivo.id, id_usuario=usuario.id, db=db)

                if favorito:
                    favorite_repo.delete_favorite_file_no_commit(
                        favorito=favorito, db=db)
                else:
                    favorito_insertar = ArchivoFavorito(
                        id_usuario=usuario.id, id_archivo=archivo.id)

                    favorite_repo.add_favorite_file_no_commit(
                        favorito=favorito_insertar, db=db)

                nombre_item = archivo.nombre_original or "desconocido"

            else:
                carpeta: Folder = folder_services.obtener_carpeta_usuario_permisos(
                    id_carpeta=item.id, usuario=usuario, db=db)

                favorito: CarpetaFavorita | None = favorite_repo.get_favorite_folder_user_by_folder_id(
                    id_carpeta=carpeta.id, id_usuario=usuario.id, db=db)

                if favorito:
                    favorite_repo.delete_favorite_folder_no_commit(
                        favorito=favorito, db=db)
                else:
                    favorito_insertar = CarpetaFavorita(
                        id_usuario=usuario.id, id_carpeta=carpeta.id)

                    favorite_repo.add_favorite_folder_no_commit(
                        favorito=favorito_insertar, db=db)

                nombre_item = carpeta.nombre_original or "desconocido"

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores
