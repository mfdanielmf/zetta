import { useDownloadStore } from '@/stores/download.store'
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
  restaurarSeleccion(data: ItemMultipleRequest) {
    return api().put(URL + '/restaurar', data)
  },
  async descargarSeleccion(data: ItemMultipleRequest) {
    const downloadStore = useDownloadStore()
    downloadStore.reset()
    downloadStore.estado = 'preparando'

    try {
      const res = await api().post(URL, data, {
        responseType: 'blob',
        onDownloadProgress: ({ loaded, total }) => {
          if (downloadStore.estado !== 'descargando') {
            downloadStore.estado = 'descargando'
          }

          downloadStore.setPorcentaje(loaded, total ?? 0)
        },
      })

      downloadStore.estado = 'completado'

      return res
    } catch (e: unknown) {
      downloadStore.estado = 'error'

      throw e
    }
  },
  cancelarCompartidoMultiple(data: ItemMultipleRequest) {
    return api().delete<MultipleItemResponse>(URL + '/shared/sent', { data })
  },
}
