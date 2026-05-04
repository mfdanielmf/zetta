import type { ShareFileRequest } from '@/api/types/types'
import {
  getReceivedFilesService,
  getSharedFilesByMeService,
  shareFileService,
} from '@/services/shared/shared.files.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { toast } from 'vue-sonner'

export function useGetSharedFilesByMe() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosCompartidos', authStore.usuario?.id],
    queryFn: () => getSharedFilesByMeService(),
    enabled: !!authStore.usuario?.id,
  })
}

export function useShareFile() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ShareFileRequest) => shareFileService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['itemsCompartidos'],
      })

      toast.success(data?.msg || 'Se ha compartido el archivo correctamente')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al compartir el archivo')
      } else {
        toast.error('Error al compartir el archivo')
      }
    },
  })
}

export function useGetReceivedFiles() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosRecibidos', authStore.usuario?.id],
    queryFn: () => getReceivedFilesService(),
    enabled: !!authStore.usuario?.id,
  })
}
