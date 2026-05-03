import api from '../axios.config'
import type { GetItemsResponse } from '../types/types'

const URL = '/api/v2/items'

export default {
  obtenerItems(params: { pagina: number; limite: number }) {
    return api().get<GetItemsResponse>(URL, { params: params })
  },
}
