import { getFilesUserService } from "@/services/file.services";
import { useQuery } from "@tanstack/vue-query";

export function useGetFilesUser(){
  return useQuery({
    queryKey: ["archivos"],
    queryFn: () => getFilesUserService()
  })
}
