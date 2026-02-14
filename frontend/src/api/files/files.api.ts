import api from "../axios.config";
import type { GetFilesResponse } from "../types/types";

export default {
  obtenerArchivosUsuario(){
    return api().get<GetFilesResponse>('/api/files')
  }
}
