import filesApi from "@/api/files/files.api"
import axios from "axios"
import { toast } from "vue-sonner"

export async function getFilesUserService(){
  try{
    const req = await filesApi.obtenerArchivosUsuario()

    return req.data
  }catch(e: unknown){
    if (axios.isAxiosError(e)){
      toast.error(e.response?.data?.detail || "Error al obtener los archivos")
    }else{
      toast.error("Error al obtener los archivos")
    }
  }
}
