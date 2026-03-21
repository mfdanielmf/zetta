import {
  crearCarpetasService,
  obtenerArchivosCarpetaService,
  obtenerCarpetasService,
  subirArchivoCarpetaService,
} from '@/services/folder.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { toast } from 'vue-sonner'

export function useCreateFolder() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (nombre: string) => crearCarpetasService(nombre),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['carpetas', authStore.usuario?.id] })

      toast.success(data?.msg || 'Se ha creado la carpeta correctamente')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al crear la carpeta')
      } else {
        toast.error('Error al crear la carpeta')
      }
    },
  })
}

export function useGetFoldersUser() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['carpetas', authStore.usuario?.id],
    queryFn: () => obtenerCarpetasService(),
    enabled: !!authStore.usuario?.id,
  })
}

export function useGetFilesFolder(idCarpeta: string) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosCarpeta', authStore.usuario?.id, idCarpeta],
    queryFn: () => obtenerArchivosCarpetaService(idCarpeta),
    enabled: !!authStore.usuario?.id && !!idCarpeta,
  })
}

export function useUploadFileFolder() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: ({ idCarpeta, data }: { idCarpeta: string; data: FormData }) =>
      subirArchivoCarpetaService(idCarpeta, data),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({
        queryKey: ['archivosCarpeta', authStore.usuario?.id, variables.idCarpeta],
      })

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
