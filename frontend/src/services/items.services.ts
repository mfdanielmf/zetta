import itemsApi from '@/api/items/items.api'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function getItemsService(pagina: number, limite: number) {
  try {
    const req = await itemsApi.obtenerItems({ pagina, limite })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos y carpetas')
    } else {
      toast.error('Error al obtener los archivos y carpetas')
    }
  }
}

export async function getItemsFolderService(idCarpeta: string, pagina: number, limite: number) {
  try {
    const req = await itemsApi.obtenerItemsCarpeta(idCarpeta, { pagina, limite })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los detalles de la carpeta')
    } else {
      toast.error('Error al obtener los detalles de la carpeta')
    }
  }
}

export async function getItemsTrashService(pagina: number, limite: number) {
  try {
    const req = await itemsApi.obtenerItemsPapelera({ pagina, limite })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los detalles de la papelera')
    } else {
      toast.error('Error al obtener los detalles de la papelera')
    }
  }
}

export async function getItemsFolderTrashService(
  idCarpeta: string,
  pagina: number,
  limite: number,
) {
  try {
    const req = await itemsApi.obtenerItemsCarpetaPapelera(idCarpeta, { pagina, limite })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los detalles de la carpeta')
    } else {
      toast.error('Error al obtener los detalles de la carpeta')
    }
  }
}

export async function getReceivedItemsService(pagina: number, limite: number) {
  try {
    const req = await itemsApi.obtenerItemsRecibidos({ pagina, limite })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos y carpetas recibidos')
    } else {
      toast.error('Error al obtener los archivos y carpetas recibidos')
    }
  }
}

export async function getSentItemsService(pagina: number, limite: number) {
  try {
    const req = await itemsApi.obtenerItemsCompartidos({ pagina, limite })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(
        e.response?.data?.detail || 'Error al obtener los archivos y carpetas compartidos',
      )
    } else {
      toast.error('Error al obtener los archivos y carpetas compartidos')
    }
  }
}
