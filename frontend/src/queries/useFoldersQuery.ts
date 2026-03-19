import {
  crearCarpetasService,
  obtenerArchivosCarpetaService,
  obtenerCarpetasService,
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

export function useGetFilesFolder(id_carpeta: string) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosCarpeta', authStore.usuario?.id, id_carpeta],
    queryFn: () => obtenerArchivosCarpetaService(id_carpeta),
    enabled: !!authStore.usuario?.id && !!id_carpeta,
  })
}
