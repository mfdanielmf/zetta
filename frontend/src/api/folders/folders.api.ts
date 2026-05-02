import api from '../axios.config'
import type {
  CreateFolderAnidadaResponse,
  CreateFolderResponse,
  DeleteFolderPermanentResponse,
  GetFilesFolderResponse,
  GetFilesFolderTrashResponse,
  GetFoldersAnidada,
  GetFoldersAnidadaTrashResponse,
  GetFoldersResponse,
  GetFoldersTrashResponse,
  RestoreFolderResponse,
  SendFolderTrashResponse,
  UploadFileFolderResponse,
} from '../types/types'

const URL = '/api/folders'

export default {
  crearCarpeta(nombreCarpeta: string) {
    return api().post<CreateFolderResponse>(URL, { nombre_carpeta: nombreCarpeta })
  },
  obtenerCarpetasUsuario() {
    return api().get<GetFoldersResponse>(URL)
  },
  obtenerArchivosCarpeta(idCarpeta: string) {
    return api().get<GetFilesFolderResponse>(URL + `/${idCarpeta}/files`)
  },
  subirArchivosCarpeta(idCarpeta: string, data: FormData) {
    return api().post<UploadFileFolderResponse>(URL + `/${idCarpeta}/files`, data)
  },
  crearCarpetaAnidada(idCarpetaPadre: string, nombreCarpeta: string) {
    return api().post<CreateFolderAnidadaResponse>(URL + `/${idCarpetaPadre}/folders`, {
      nombre_carpeta: nombreCarpeta,
    })
  },
  obtenerCarpetasAnidadas(idCarpeta: string) {
    return api().get<GetFoldersAnidada>(URL + `/${idCarpeta}/folders`)
  },
  mandarCarpetaPapelera(idCarpeta: string) {
    return api().delete<SendFolderTrashResponse>(URL + `/${idCarpeta}`)
  },
  obtenerCarpetasPapelera() {
    return api().get<GetFoldersTrashResponse>(URL + '/trash')
  },
  restaurarCarpetaPapelera(idCarpeta: string) {
    return api().put<RestoreFolderResponse>(URL + `/${idCarpeta}/restaurar`)
  },
  eliminarCarpetaPermanente(idCarpeta: string) {
    return api().delete<DeleteFolderPermanentResponse>(URL + `/trash/${idCarpeta}`)
  },
  obtenerArchivosCarpetaPapelera(idCarpeta: string) {
    return api().get<GetFilesFolderTrashResponse>(URL + `/trash/${idCarpeta}/files`)
  },
  obtenerCarpetasAnidadasPapelera(idCarpeta: string) {
    return api().get<GetFoldersAnidadaTrashResponse>(URL + `/trash/${idCarpeta}/folders`)
  },
  descargarCarpeta(idCarpeta: string) {
    return api().get(URL + `/${idCarpeta}`, { responseType: 'blob' })
  },
}
