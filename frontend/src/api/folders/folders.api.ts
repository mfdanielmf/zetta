import api from '../axios.config'
import type {
  CreateFolderResponse,
  GetFilesFolderResponse,
  GetFoldersResponse,
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
}
