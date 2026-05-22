import { obtenerFavoritosService } from '@/services/favorite.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'
import type { Ref } from 'vue'

export function useGetFavoriteItems(
  pagina: Ref<number>,
  limite: number = 25,
  busqueda: Ref<string>,
) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['favoritos', authStore.usuario?.id, pagina, busqueda],
    queryFn: () => obtenerFavoritosService(pagina.value, limite, busqueda.value),
    enabled: !!authStore.usuario?.id,
  })
}
