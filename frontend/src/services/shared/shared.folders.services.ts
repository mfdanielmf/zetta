import sharedApi from '@/api/shared/shared.api'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function getSharedFoldersByMeService() {
  try {
    const req = await sharedApi.obtenerCarpetasCompartidasPorMi()

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener las carpetas compartidas')
    } else {
      toast.error('Error al obtener las carpetas compartidas')
    }
  }
}
