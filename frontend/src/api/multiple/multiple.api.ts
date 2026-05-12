import api from '../axios.config'
import type { ItemMultipleRequest, MultipleItemResponse } from '../types/types'

const URL = '/api/v2/multiple/items'

export default {
  mandarPapeleraSeleccion(data: ItemMultipleRequest) {
    return api().delete<MultipleItemResponse>(URL, { data })
  },
}
