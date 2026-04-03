import {
  getFilesUserService,
  insertarFilesService,
  sendFileTrashService,
} from '@/services/file.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { toast } from 'vue-sonner'

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
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['archivos', authStore.usuario?.id] })

      toast.success(data?.msg || 'Se han subido los archivos correctamente')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al subir los archivos')
      } else {
        toast.error('Error al subir los archivos')
      }
    },
  })
}

//DEVNOTES:
//Acordarme de invalidar queries cuando tenga hecha la lógica de que solo se muestren archivos no eliminados y demás
export function useMoveFileTrash() {
  return useMutation({
    mutationFn: (idArchivo: string) => sendFileTrashService(idArchivo),
    onSuccess: (data) => {
      toast.success(data?.msg || 'Archivo eliminado correctamente. Puedes verlo en la papelera')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al eliminar el archivo')
      } else {
        toast.error('Error al eliminar el archivo')
      }
    },
  })
}
