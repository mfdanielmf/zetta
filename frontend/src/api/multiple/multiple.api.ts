import api from '../axios.config'
import type {
  ItemMultipleRequest,
  MultipleItemResponse,
  ShareMultipleItemsRequest,
  ShareMultipleItemsResponse,
} from '../types/types'

const URL = '/api/v2/multiple/items'

export default {
  mandarPapeleraSeleccion(data: ItemMultipleRequest) {
    return api().delete<MultipleItemResponse>(URL, { data })
  },
  compartirSeleccion(data: ShareMultipleItemsRequest) {
    return api().post<ShareMultipleItemsResponse>(URL + '/sent', data)
  },
  eliminarDefinitivoSeleccion(data: ItemMultipleRequest) {
    return api().delete<MultipleItemResponse>(URL + '/trash', { data })
  },
}
