import favoritesApi from '@/api/favorites/favorites.api'
import axios from 'axios'
import { toast } from 'vue-sonner'

export async function obtenerFavoritosService(pagina: number, limite: number, busqueda: string) {
  try {
    const req = await favoritesApi.obtenerFavoritos({ pagina, limite, busqueda })

    return req.data
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al obtener los favoritos')
    } else {
      toast.error('Error al obtener los favoritos')
    }
  }
}
