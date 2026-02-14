import { getFilesUserService } from "@/services/files.services";
import { useQuery } from "@tanstack/vue-query";

export function useGetFilesUser(){
  return useQuery({
    queryKey: ["archivos"],
    queryFn: () => getFilesUserService()
  })
}
