import multipleApi from '@/api/multiple/multiple.api'
import type { ItemMultipleRequest } from '@/api/types/types'

export async function sendItemsTrashService(data: ItemMultipleRequest) {
  const req = await multipleApi.mandarPapeleraSeleccion(data)

  return req.data
}
