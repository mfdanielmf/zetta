import { getFilesUserService } from "@/services/file.services";
import { useAuthStore } from "@/stores/auth.store";
import { useQuery } from "@tanstack/vue-query";

export function useGetFilesUser(){
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ["archivos", authStore.usuario?.id],
    queryFn: () => getFilesUserService(),
    enabled: !!authStore.usuario?.id
  })
}
