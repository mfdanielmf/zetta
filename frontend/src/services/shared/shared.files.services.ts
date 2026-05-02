import sharedApi from '@/api/shared/shared.api'
import type { ShareFileRequest } from '@/api/types/types'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function getSharedFilesByMeService() {
  try {
    const req = await sharedApi.obtenerArchivosCompartidosPorMi()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos compartidos')
    } else {
      toast.error('Error al obtener los archivos compartidos')
    }
  }
}

export async function shareFileService(data: ShareFileRequest) {
  const req = await sharedApi.compartirArchivo(data)

  return req.data
}

export async function getReceivedFilesService() {
  try {
    const req = await sharedApi.obtenerArchivosRecibidos()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos recibidos')
    } else {
      toast.error('Error al obtener los archivos recibidos')
    }
  }
}
