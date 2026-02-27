import { crearCarpetasService } from "@/services/folder.services";
import { useAuthStore } from "@/stores/auth.store";
import { useQuery } from "@tanstack/vue-query";

export function useCreateFolder(nombre: string){
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ["carpetas", authStore.usuario?.id],
    queryFn: () => crearCarpetasService(nombre),
    enabled: !!authStore.usuario?.id
  })
}
