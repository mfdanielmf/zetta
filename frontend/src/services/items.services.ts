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
