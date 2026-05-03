import itemsApi from '@/api/items/items.api'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function getItemsService() {
  try {
    const req = await itemsApi.obtenerItems()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los archivos y carpetas')
    } else {
      toast.error('Error al obtener los archivos y carpetas')
    }
  }
}
