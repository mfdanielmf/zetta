import { getItemsService } from '@/services/items.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'
import type { Ref } from 'vue'

export function useGetItemsUser(pagina: Ref<number>, limite: number = 25) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['items', authStore.usuario?.id, pagina],
    queryFn: () => getItemsService(pagina.value, limite),
    enabled: !!authStore.usuario?.id,
  })
}
