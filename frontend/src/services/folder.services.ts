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

export async function obtenerArchivosCarpetaService(idCarpeta: string) {
  // Try catch manejado en el guard del router
  const req = await foldersApi.obtenerArchivosCarpeta(idCarpeta)

  return req.data
}

export async function subirArchivoCarpetaService(idCarpeta: string, data: FormData) {
  const req = await foldersApi.subirArchivosCarpeta(idCarpeta, data)

  return req.data
}

export async function crearCarpetaAnidadaService(idCarpetaPadre: string, nombreCarpeta: string) {
  const req = await foldersApi.crearCarpetaAnidada(idCarpetaPadre, nombreCarpeta)

  return req.data
}
