import api from '../axios.config'
import type {
  GetFolderItemsResponse,
  GetItemsResponse,
  GetItemsTrashResponse,
} from '../types/types'

const URL = '/api/v2/items'

export default {
  obtenerItems(params: { pagina: number; limite: number }) {
    return api().get<GetItemsResponse>(URL, { params: params })
  },
  obtenerItemsCarpeta(idCarpeta: string, params: { pagina: number; limite: number }) {
    return api().get<GetFolderItemsResponse>(URL + `/${idCarpeta}/items`, { params: params })
  },
  obtenerItemsPapelera(params: { pagina: number; limite: number }) {
    return api().get<GetItemsTrashResponse>(URL + '/trash', { params: params })
  },
}
