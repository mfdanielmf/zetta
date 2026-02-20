import { getFilesUserService, insertarFilesService } from '@/services/file.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

export function useGetFilesUser() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivos', authStore.usuario?.id],
    queryFn: () => getFilesUserService(),
    enabled: !!authStore.usuario?.id,
  })
}

export function useInsertFiles() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (data: FormData) => insertarFilesService(data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ['archivos', authStore.usuario?.id] }),
  })
}
