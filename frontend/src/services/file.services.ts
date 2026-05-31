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
  if (!bytes) return '0 B'

  const unidades = ['B', 'KB', 'MB', 'GB', 'TB']
  const k = 1024

  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${Number.parseFloat((bytes / k ** i).toFixed(decimales))} ${unidades[i]}`
}

export async function insertarFilesService(data: FormData) {
  const req = await filesApi.subirArchivosUsuario(data)

  return req.data
}

export async function downloadFileService(id: string, nombre: string) {
  try {
    const req = await filesApi.descargarArchivo(id, nombre)

    const contentType =
      typeof req.headers['content-type'] === 'string'
        ? req.headers['content-type']
        : 'application/octet-stream'

    const blob = new Blob([req.data], {
      type: contentType,
    })

    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', nombre)
    document.body.appendChild(link)
    link.click()
    link.remove()

    setTimeout(() => URL.revokeObjectURL(url), 2000)
  } catch {
    toast.error('Ha ocurrido un error al descargar los archivos')
  }
}

export async function sendFileTrashService(idArchivo: string) {
  const req = await filesApi.mandarArchivoPapelera(idArchivo)

  return req.data
}

export async function getFilesTrashService() {
  try {
    const req = await filesApi.obtenerArchivosPapelera()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos')
    } else {
      toast.error('Error al obtener los archivos')
    }
  }
}

export async function restoreFileService(idArchivo: string) {
  const req = await filesApi.restaurarArchivoPapelera(idArchivo)

  return req.data
}

export async function deleteFilePermanentService(idArchivo: string) {
  const req = await filesApi.eliminarArchivoPermanente(idArchivo)

  return req.data
}
