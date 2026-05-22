import type { Params } from '@/types/types'
import api from '../axios.config'
import type {
  GetFolderItemsResponse,
  GetItemsFolderTrashResponse,
  GetItemsResponse,
  GetItemsTrashResponse,
  GetReceivedItemsResponse,
  GetSentItemsResponse,
} from '../types/types'

const URL = '/api/v2/items'

export default {
  obtenerItems(params: Params) {
    return api().get<GetItemsResponse>(URL, { params })
  },
  obtenerItemsCarpeta(idCarpeta: string, params: Params) {
    return api().get<GetFolderItemsResponse>(URL + `/${idCarpeta}/items`, { params })
  },
  obtenerItemsPapelera(params: Params) {
    return api().get<GetItemsTrashResponse>(URL + '/trash', { params })
  },
  obtenerItemsCarpetaPapelera(idCarpeta: string, params: Params) {
    return api().get<GetItemsFolderTrashResponse>(URL + `/trash/${idCarpeta}/items`, {
      params: params,
    })
  },
  obtenerItemsRecibidos(params: Params) {
    return api().get<GetReceivedItemsResponse>(URL + '/shared/received', { params })
  },
  obtenerItemsCompartidos(params: Params) {
    return api().get<GetSentItemsResponse>(URL + '/shared/sent', { params })
  },
}
