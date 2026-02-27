import foldersApi from "@/api/folders/folders.api"
import axios from "axios"
import { toast } from "vue-sonner"

export async function crearCarpetasService(nombre: string) {
  try {
    const req = await foldersApi.crearCarpeta(nombre)

    toast.success(req.data.msg)
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) {
      toast.error(e.response?.data?.detail || 'Error al crear la carpeta')
    } else {
      toast.error('Error al crear la carpeta')
    }
  }
}
