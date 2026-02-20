import api from '../axios.config'
import type { GetFilesResponse, PostFilesResponse } from '../types/types'

export default {
  obtenerArchivosUsuario() {
    return api().get<GetFilesResponse>('/api/files')
  },
  subirArchivosUsuario(data: FormData) {
    return api().post<PostFilesResponse>('/api/files', data)
  },
}
