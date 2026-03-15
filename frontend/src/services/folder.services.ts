import foldersApi from '@/api/folders/folders.api'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function crearCarpetasService(nombre: string) {
  const req = await foldersApi.crearCarpeta(nombre)

  return req.data
}

export async function obtenerCarpetasService() {
  try {
    const req = await foldersApi.obtenerCarpetasUsuario()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener las carpetas')
    } else {
      toast.error('Error al obtener los archivos')
    }
  }
}

export async function obtenerArchivosCarpetaService(id_carpeta: string) {
  try {
    const req = await foldersApi.obtenerArchivosCarpeta(id_carpeta)

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos de la carpeta')
    } else {
      toast.error('Error al obtener los archivos de la carpeta')
    }
  }
}
