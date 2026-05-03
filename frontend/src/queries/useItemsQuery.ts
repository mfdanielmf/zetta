import {
  getItemsFolderService,
  getItemsService,
  getItemsTrashService,
} from '@/services/items.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'
import { computed, type ComputedRef, type Ref } from 'vue'

export function useGetItemsUser(pagina: Ref<number>, limite: number = 25) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['items', authStore.usuario?.id, pagina],
    queryFn: () => getItemsService(pagina.value, limite),
    enabled: !!authStore.usuario?.id,
  })
}

export function useGetFolderItems(
  idCarpeta: ComputedRef<string>,
  pagina: Ref<number>,
  limite: number = 25,
) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['itemsCarpeta', authStore.usuario?.id, idCarpeta, pagina],
    queryFn: () => getItemsFolderService(idCarpeta.value, pagina.value, limite),
    enabled: computed(() => !!authStore.usuario?.id && !!idCarpeta.value),
  })
}

export function useGetItemsPapelera(pagina: Ref<number>, limite: number = 25) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['itemsPapelera', authStore.usuario?.id, pagina],
    queryFn: () => getItemsTrashService(pagina.value, limite),
    enabled: !!authStore.usuario?.id,
  })
}
