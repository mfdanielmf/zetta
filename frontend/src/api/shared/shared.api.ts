import api from '../axios.config'
import type { GetSharedFilesByMeResponse, GetSharedFoldersByMeResponse } from '../types/types'

const URL = '/api/shared'

export default {
  obtenerArchivosCompartidosPorMi() {
    return api().get<GetSharedFilesByMeResponse>(URL + '/sent/files')
  },
  obtenerCarpetasCompartidasPorMi() {
    return api().get<GetSharedFoldersByMeResponse>(URL + '/sent/folders')
  },
}
