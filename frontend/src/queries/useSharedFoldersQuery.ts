import type { ShareFolderRequest } from '@/api/types/types'
import {
  getSharedFoldersByMeService,
  shareFolderService,
} from '@/services/shared/shared.folders.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { toast } from 'vue-sonner'

export function useGetSharedFoldersByMe() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['carpetasCompartidas', authStore.usuario?.id],
    queryFn: () => getSharedFoldersByMeService(),
    enabled: !!authStore.usuario?.id,
  })
}

export function useShareFolder() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (data: ShareFolderRequest) => shareFolderService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['carpetasCompartidas', authStore.usuario?.id] })

      toast.success(data?.msg || 'Se ha compartido la carpeta correctamente')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al compartir la carpeta')
      } else {
        toast.error('Error al compartir la carpeta')
      }
    },
  })
}
