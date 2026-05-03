import { getItemsService } from '@/services/items.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'

export function useGetItemsUser() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['items', authStore.usuario?.id],
    queryFn: () => getItemsService(),
    enabled: !!authStore.usuario?.id,
  })
}
