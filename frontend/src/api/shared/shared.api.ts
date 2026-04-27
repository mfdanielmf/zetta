import api from '../axios.config'
import type {
  GetSharedFilesByMeResponse,
  GetSharedFoldersByMeResponse,
  ShareFileRequest,
  ShareFileResponse,
  ShareFolderRequest,
  ShareFolderResponse,
} from '../types/types'

const URL = '/api/shared'

export default {
  obtenerArchivosCompartidosPorMi() {
    return api().get<GetSharedFilesByMeResponse>(URL + '/sent/files')
  },
  compartirArchivo(req: ShareFileRequest) {
    return api().post<ShareFileResponse>(URL + '/sent/files', {
      id_archivo: req.id_archivo,
      correo_usuario: req.correo_usuario,
    })
  },
  obtenerCarpetasCompartidasPorMi() {
    return api().get<GetSharedFoldersByMeResponse>(URL + '/sent/folders')
  },
  compartirCarpeta(req: ShareFolderRequest) {
    return api().post<ShareFolderResponse>(URL + '/sent/folders', {
      id_carpeta: req.id_carpeta,
      correo_usuario: req.correo_usuario,
    })
  },
}
