import multipleApi from '@/api/multiple/multiple.api'
import type { ItemMultipleRequest, ShareMultipleItemsRequest } from '@/api/types/types'

export async function sendItemsTrashService(data: ItemMultipleRequest) {
  const req = await multipleApi.mandarPapeleraSeleccion(data)

  return req.data
}

export async function shareMultipleItemsService(data: ShareMultipleItemsRequest) {
  const req = await multipleApi.compartirSeleccion(data)

  return req.data
}
