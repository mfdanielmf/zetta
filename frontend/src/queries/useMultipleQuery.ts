import type { ItemMultipleRequest, ShareMultipleItemsRequest } from '@/api/types/types'
import {
  cancelMultipleSharesService,
  deleteMultipleItemsService,
  restoreMultipleItemsService,
  sendItemsTrashService,
  shareMultipleItemsService,
  toggleFavoriteMultipleService,
} from '@/services/multiple.services'
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

      queryClient.invalidateQueries({
        queryKey: ['itemsCarpeta'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCarpetaPapelera'],
      })

      queryClient.invalidateQueries({
        queryKey: ['favoritos'],
      })

      toast.success(data?.msg || 'Proceso completado correctamente', {
        description:
          `Items procesados: ${data.items_totales} | Errores: ${data.errores?.total_errores ? data.errores?.total_errores : 0}` ||
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

export function useShareMultiple() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ShareMultipleItemsRequest) => shareMultipleItemsService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['itemsCompartidos'],
      })

      toast.success(data?.msg || 'Proceso completado correctamente', {
        description:
          `Items procesados: ${data.items_totales} | Errores: ${data.errores?.total_errores ? data.errores?.total_errores : 0}` ||
          '',
      })
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al compartir la selección')
      } else {
        toast.error('Error al compartir la selección')
      }
    },
  })
}

export function useDeleteMultiplePermanent() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ItemMultipleRequest) => deleteMultipleItemsService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['itemsPapelera'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCompartidos'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCarpetaPapelera'],
      })

      toast.success(data?.msg || 'Proceso completado correctamente', {
        description:
          `Items procesados: ${data.items_totales} | Errores: ${data.errores?.total_errores ? data.errores?.total_errores : 0}` ||
          '',
      })
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al eliminar la selección')
      } else {
        toast.error('Error al eliminar la selección')
      }
    },
  })
}

export function useRestoreMultiple() {
  const authStore = useAuthStore()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ItemMultipleRequest) => restoreMultipleItemsService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['items', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsPapelera'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCarpeta'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCarpetaPapelera'],
      })

      queryClient.invalidateQueries({
        queryKey: ['favoritos'],
      })

      toast.success(data?.msg || 'Proceso completado correctamente', {
        description:
          `Items procesados: ${data.items_totales} | Errores: ${data.errores?.total_errores ? data.errores?.total_errores : 0}` ||
          '',
      })
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al restaurar la selección')
      } else {
        toast.error('Error al restaurar la selección')
      }
    },
  })
}

export function useCancelMultipleShared() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ItemMultipleRequest) => cancelMultipleSharesService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['itemsCompartidos'],
      })

      toast.success(data?.msg || 'Proceso completado correctamente', {
        description:
          `Items procesados: ${data.items_totales} | Errores: ${data.errores?.total_errores ? data.errores?.total_errores : 0}` ||
          '',
      })
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al cancelar compartido')
      } else {
        toast.error('Error al cancelar compartido')
      }
    },
  })
}

export function useToggleFavoriteMultiple() {
  const authStore = useAuthStore()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ItemMultipleRequest) => toggleFavoriteMultipleService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['items', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['favoritos'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCarpeta'],
      })

      queryClient.invalidateQueries({
        queryKey: ['itemsCompartidos'],
      })

      if (data.errores && data.errores.total_errores > 0) {
        toast.error('Error al actualizar el estado favorito')
      } else {
        toast.success('Favorito actualizado')
      }
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al actualizar el estado favorito')
      } else {
        toast.error('Error al actualizar el estado favorito')
      }
    },
  })
}
