import {
  deleteFilePermanentService,
  getFilesTrashService,
  getFilesUserService,
  insertarFilesService,
  restoreFileService,
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
  // const authStore = useAuthStore()

  return useMutation({
    mutationFn: (data: FormData) => insertarFilesService(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['items'] })

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

export function useMoveFileTrash() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (idArchivo: string) => sendFileTrashService(idArchivo),
    onSuccess: (data) => {
      //Invalidar archivos del almacenamiento y archivos de la papelera
      queryClient.invalidateQueries({
        queryKey: ['items', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['archivosPapelera', authStore.usuario?.id],
      })

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

export function useGetFilesTrash() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosPapelera', authStore.usuario?.id],
    queryFn: () => getFilesTrashService(),
    enabled: !!authStore.usuario?.id,
  })
}

export function useRestoreFile() {
  const authStore = useAuthStore()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (idArchivo: string) => restoreFileService(idArchivo),
    onSuccess: (data) => {
      //Invalidar archivos del almacenamiento y archivos de la papelera
      queryClient.invalidateQueries({
        queryKey: ['items', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['archivosPapelera', authStore.usuario?.id],
      })

      toast.success(data?.msg || 'Archivo restaurado correctamente')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al restaurar el archivo')
      } else {
        toast.error('Error al restaurar el archivo')
      }
    },
  })
}

export function useDeleteFilePermanent() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (idArchivo: string) => deleteFilePermanentService(idArchivo),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['archivosPapelera', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['archivosCompartidos', authStore.usuario?.id],
      })

      toast.success(data?.msg || 'Archivo eliminado correctamente')
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
