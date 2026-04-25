import { getSharedFilesByMeService } from '@/services/shared/shared.files.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'

export function useGetSharedFilesByMe() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosCompartidos', authStore.usuario?.id],
    queryFn: () => getSharedFilesByMeService(),
    enabled: !!authStore.usuario?.id,
  })
}
