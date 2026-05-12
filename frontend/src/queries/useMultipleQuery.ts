import type { ItemMultipleRequest } from '@/api/types/types'
import { sendItemsTrashService } from '@/services/multiple.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { toast } from 'vue-sonner'

export function useMoveSelectedTrash() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (data: ItemMultipleRequest) => sendItemsTrashService(data),
    onSuccess: (data) => {
      //Invalidar archivos del almacenamiento y archivos de la papelera
      queryClient.invalidateQueries({
        queryKey: ['items', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsPapelera'],
      })

      toast.success(data?.msg || 'Proceso completado correctamente', {
        description:
          `Items eliminados: ${data.items_totales} | Errores: ${data.errores?.total_errores ? data.errores?.total_errores : 0}` ||
          '',
      })
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al mandar a la papelera')
      } else {
        toast.error('Error al mandar a la papelera')
      }
    },
  })
}
