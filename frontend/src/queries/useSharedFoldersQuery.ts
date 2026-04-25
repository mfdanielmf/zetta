import { getSharedFoldersByMeService } from '@/services/shared/shared.folders.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'

export function useGetSharedFoldersByMe() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['carpetasCompartidas', authStore.usuario?.id],
    queryFn: () => getSharedFoldersByMeService(),
    enabled: !!authStore.usuario?.id,
  })
}
