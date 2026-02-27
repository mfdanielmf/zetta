import { crearCarpetasService } from "@/services/folder.services";
import { useMutation} from "@tanstack/vue-query";

export function useCreateFolder(){
  return useMutation({
    mutationFn: (nombre: string) => crearCarpetasService(nombre)
  })
}
