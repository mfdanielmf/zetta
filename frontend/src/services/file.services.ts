import filesApi from '@/api/files/files.api'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function getFilesUserService() {
  try {
    const req = await filesApi.obtenerArchivosUsuario()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos')
    } else {
      toast.error('Error al obtener los archivos')
    }
  }
}

export function formatDateService(fecha: string) {
  const date = new Date(fecha)

  return date.toLocaleDateString('es-ES') + ' ' + date.toLocaleTimeString('es-ES')
}

export function formatearTamañoService(bytes: number, decimales: number = 2) {
  const unidades = ['B', 'KB', 'MB', 'GB', 'TB']
  const k = 1024

  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${Number.parseFloat((bytes / k ** i).toFixed(decimales))} ${unidades[i]}`
}

export async function insertarFilesService(data: FormData) {
  const req = await filesApi.subirArchivosUsuario(data)

  return req.data
}
