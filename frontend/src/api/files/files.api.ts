import api from '../axios.config'
import type { GetFilesResponse, GetFilesTrashResponse, PostFilesResponse, SendFileTrashResponse } from '../types/types'

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
  mandarArchivoPapelera(idArchivo: string) {
    return api().delete<SendFileTrashResponse>(URL + `/${idArchivo}`)
  },
  obtenerArchivosPapelera(){
    return api().get<GetFilesTrashResponse>(URL + "/trash")
  }
}
