import api from '../axios.config'
import type {
  CreateFolderAnidadaResponse,
  CreateFolderResponse,
  GetFilesFolderResponse,
  GetFoldersAnidada,
  GetFoldersResponse,
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
}
