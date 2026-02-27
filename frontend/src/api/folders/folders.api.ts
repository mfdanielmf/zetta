import api from "../axios.config"
import type { CreateFolderResponse } from '../types/types'

const URL = '/api/folders'

export default {
  crearCarpeta(nombre_carpeta: string){
    return api().post<CreateFolderResponse>(URL, nombre_carpeta)
  }
}
