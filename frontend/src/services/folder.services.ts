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
      toast.error('Error al obtener las carpetas')
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

export async function obtenerCarpetasAnidadasService(idCarpeta: string) {
  try {
    const req = await foldersApi.obtenerCarpetasAnidadas(idCarpeta)

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener las carpetas')
    } else {
      toast.error('Error al obtener los carpetas')
    }
  }
}

export async function sendFolderTrashService(idCarpeta: string) {
  const req = await foldersApi.mandarCarpetaPapelera(idCarpeta)

  return req.data
}

export async function obtenerCarpetasPapeleraService() {
  try {
    const req = await foldersApi.obtenerCarpetasPapelera()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener las carpetas')
    } else {
      toast.error('Error al obtener las carpetas')
    }
  }
}

export async function restoreFolderService(idCarpeta: string) {
  const req = await foldersApi.restaurarCarpetaPapelera(idCarpeta)

  return req.data
}

export async function deleteFolderPermanentService(idCarpeta: string) {
  const req = await foldersApi.eliminarCarpetaPermanente(idCarpeta)

  return req.data
}

export async function obtenerArchivosCarpetaPapeleraService(idCarpeta: string) {
  try {
    const req = await foldersApi.obtenerArchivosCarpetaPapelera(idCarpeta)

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos')
    } else {
      toast.error('Error al obtener los archivos')
    }
  }
}

export async function obtenerCarpetasAnidadasPapeleraService(idCarpeta: string) {
  try {
    const req = await foldersApi.obtenerCarpetasAnidadasPapelera(idCarpeta)

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener las carpetas')
    } else {
      toast.error('Error al obtener los carpetas')
    }
  }
}

export async function downloadFolderService(id: string, nombre: string) {
  try {
    const req = await foldersApi.descargarCarpeta(id)

    const blob = new Blob([req.data], {
      type: req.headers['content-type'],
    })

    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', nombre)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch {
    toast.error('Ha ocurrido un error al descargar la carpeta')
  }
}
