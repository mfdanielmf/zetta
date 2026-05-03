import api from '../axios.config'
import type { GetItemsResponse } from '../types/types'

const URL = '/api/v2/items'

export default {
  obtenerItems() {
    return api().get<GetItemsResponse>(URL)
  },
}
