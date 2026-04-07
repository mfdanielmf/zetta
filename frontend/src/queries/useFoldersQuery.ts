import {
  crearCarpetaAnidadaService,
  crearCarpetasService,
  obtenerArchivosCarpetaService,
  obtenerCarpetasAnidadasService,
  obtenerCarpetasPapeleraService,
  obtenerCarpetasService,
  restoreFolderService,
  sendFolderTrashService,
  subirArchivoCarpetaService,
} from '@/services/folder.services'
import { useAuthStore } from '@/stores/auth.store'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { computed, toValue, type ComputedRef } from 'vue'
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

export function useGetFilesFolder(idCarpeta: ComputedRef<string>) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['archivosCarpeta', authStore.usuario?.id, () => toValue(idCarpeta)],
    queryFn: () => obtenerArchivosCarpetaService(toValue(idCarpeta)),
    enabled: computed(() => !!authStore.usuario?.id && !!toValue(idCarpeta)),
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

export function useCreateFolderAnidada() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: ({
      idCarpetaPadre,
      nombreCarpeta,
    }: {
      idCarpetaPadre: string
      nombreCarpeta: string
    }) => crearCarpetaAnidadaService(idCarpetaPadre, nombreCarpeta),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({
        queryKey: ['carpetasAnidadas', authStore.usuario?.id, variables.idCarpetaPadre],
      })

      toast.success(data?.msg || 'Carpeta creada correctamente')
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

export function useGetFoldersAnidadas(idCarpeta: ComputedRef<string>) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['carpetasAnidadas', authStore.usuario?.id, () => toValue(idCarpeta)],
    queryFn: () => obtenerCarpetasAnidadasService(toValue(idCarpeta)),
    enabled: computed(() => !!authStore.usuario?.id && !!toValue(idCarpeta)),
  })
}

export function useMoveFolderTrash() {
  const queryClient = useQueryClient()
  const authStore = useAuthStore()

  return useMutation({
    mutationFn: (idCarpeta: string) => sendFolderTrashService(idCarpeta),
    onSuccess: (data, idCarpeta) => {
      queryClient.invalidateQueries({
        queryKey: ['carpetas', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['carpetasPapelera', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['archivosCarpeta', authStore.usuario?.id, idCarpeta],
      })

      queryClient.invalidateQueries({
        queryKey: ['carpetasAnidadas', authStore.usuario?.id, idCarpeta],
      })

      toast.success(data?.msg || 'Carpeta eliminada correctamente. Puedes verla en la papelera')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al eliminar la carpeta')
      } else {
        toast.error('Error al eliminar la carpeta')
      }
    },
  })
}

export function useGetFoldersTrash() {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['carpetasPapelera', authStore.usuario?.id],
    queryFn: () => obtenerCarpetasPapeleraService(),
    enabled: !!authStore.usuario?.id,
  })
}

export function useRestoreFolder() {
  const authStore = useAuthStore()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (idCarpeta: string) => restoreFolderService(idCarpeta),
    onSuccess: (data, idCarpeta) => {
      queryClient.invalidateQueries({
        queryKey: ['carpetas', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['carpetasPapelera', authStore.usuario?.id],
      })

      queryClient.invalidateQueries({
        queryKey: ['archivosCarpeta', authStore.usuario?.id, idCarpeta],
      })

      queryClient.invalidateQueries({
        queryKey: ['carpetasAnidadas', authStore.usuario?.id, idCarpeta],
      })

      toast.success(data?.msg || 'Carpeta restaurada correctamente')
    },
    onError: (e: unknown) => {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Error al restaurar la carpeta')
      } else {
        toast.error('Error al restaurar la carpeta')
      }
    },
  })
}
