import multipleApi from '@/api/multiple/multiple.api'
import type { ItemMultipleRequest, ShareMultipleItemsRequest } from '@/api/types/types'
import { toast } from 'vue-sonner'

export async function sendItemsTrashService(data: ItemMultipleRequest) {
  const req = await multipleApi.mandarPapeleraSeleccion(data)

  return req.data
}

export async function shareMultipleItemsService(data: ShareMultipleItemsRequest) {
  const req = await multipleApi.compartirSeleccion(data)

  return req.data
}

export async function deleteMultipleItemsService(data: ItemMultipleRequest) {
  const req = await multipleApi.eliminarDefinitivoSeleccion(data)

  return req.data
}

export async function restoreMultipleItemsService(data: ItemMultipleRequest) {
  const req = await multipleApi.restaurarSeleccion(data)

  return req.data
}

export async function downloadMultipleService(data: ItemMultipleRequest) {
  try {
    const req = await multipleApi.descargarSeleccion(data)

    const contentType =
      typeof req.headers['content-type'] === 'string'
        ? req.headers['content-type']
        : 'application/octet-stream'

    const blob = new Blob([req.data], { type: contentType })

    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'zetta_descarga.zip')
    document.body.appendChild(link)
    link.click()
    link.remove()

    window.URL.revokeObjectURL(url)
  } catch {
    toast.error('Ha ocurrido un error al descargar el contenido')
  }
}
