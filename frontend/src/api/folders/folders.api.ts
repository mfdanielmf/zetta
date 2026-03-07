import api from '../axios.config'
import type { CreateFolderResponse, GetFoldersResponse } from '../types/types'

const URL = '/api/folders'

export default {
  crearCarpeta(nombre_carpeta: string) {
    return api().post<CreateFolderResponse>(URL, { nombre_carpeta: nombre_carpeta })
  },
  obtenerCarpetasUsuario() {
    return api().get<GetFoldersResponse>(URL)
  },
}
