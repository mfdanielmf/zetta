import { crearCarpetasService } from '@/services/folder.services'
import { useMutation } from '@tanstack/vue-query'
import axios from 'axios'
import { toast } from 'vue-sonner'

export function useCreateFolder() {
  return useMutation({
    mutationFn: (nombre: string) => crearCarpetasService(nombre),
    onSuccess: (data) => {
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
