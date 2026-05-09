import { useUploadStore } from '@/stores/upload.store'
import api from '../axios.config'
import type {
  DeleteFilePermanentResponse,
  GetFilesResponse,
  GetFilesTrashResponse,
  PostFilesResponse,
  RestoreFileResponse,
  SendFileTrashResponse,
} from '../types/types'

const URL = '/api/files'

export default {
  obtenerArchivosUsuario() {
    return api().get<GetFilesResponse>(URL)
  },
  async subirArchivosUsuario(data: FormData) {
    const uploadStore = useUploadStore()
    uploadStore.estado = 'subiendo'

    try {
      const res = await api().post<PostFilesResponse>(URL, data, {
        onUploadProgress: ({ loaded, total }) => {
          uploadStore.setPorcentaje(loaded, total ?? 0)
        },
      })

      uploadStore.estado = 'completado'

      return res
    } catch (e: unknown) {
      uploadStore.estado = 'error'

      throw e
    }
  },
  descargarArchivo(id: string) {
    return api().get(URL + `/${id}`, { responseType: 'blob' })
  },
  mandarArchivoPapelera(idArchivo: string) {
    return api().delete<SendFileTrashResponse>(URL + `/${idArchivo}`)
  },
  obtenerArchivosPapelera() {
    return api().get<GetFilesTrashResponse>(URL + '/trash')
  },
  restaurarArchivoPapelera(idArchivo: string) {
    return api().put<RestoreFileResponse>(URL + `/${idArchivo}/restaurar`)
  },
  eliminarArchivoPermanente(idArchivo: string) {
    return api().delete<DeleteFilePermanentResponse>(URL + `/trash/${idArchivo}`)
  },
}
