import type { Params } from '@/types/types'
import api from '../axios.config'
import type { GetFavoriteItemsResponse } from '../types/types'

const URL = '/api/v2/items/favorite'

export default {
  obtenerFavoritos(params: Params) {
    return api().get<GetFavoriteItemsResponse>(URL, { params })
  },
}
