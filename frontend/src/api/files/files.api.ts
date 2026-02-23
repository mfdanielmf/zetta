import api from '../axios.config'
import type { GetFilesResponse, PostFilesResponse } from '../types/types'

const URL = '/api/files'

export default {
  obtenerArchivosUsuario() {
    return api().get<GetFilesResponse>(URL)
  },
  subirArchivosUsuario(data: FormData) {
    return api().post<PostFilesResponse>(URL, data)
  },
  descargarArchivo(id: string) {
    return api().get(URL + `/${id}`, { responseType: 'blob' })
  },
}
