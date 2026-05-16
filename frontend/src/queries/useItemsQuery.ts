import {
  getItemsFolderService,
  getItemsFolderTrashService,
  getItemsService,
  getItemsTrashService,
  getReceivedItemsService,
  getSentItemsService,
} from '@/services/items.services'
import { useAuthStore } from '@/stores/auth.store'
import { useQuery } from '@tanstack/vue-query'
import { computed, type ComputedRef, type Ref } from 'vue'

export function useGetItemsUser(pagina: Ref<number>, limite: number = 25, busqueda: Ref<string>) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['items', authStore.usuario?.id, pagina, busqueda],
    queryFn: () => getItemsService(pagina.value, limite, busqueda.value),
    enabled: !!authStore.usuario?.id,
  })
}

export function useGetFolderItems(
  idCarpeta: ComputedRef<string>,
  pagina: Ref<number>,
  limite: number = 25,
  busqueda: Ref<string>,
) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['itemsCarpeta', authStore.usuario?.id, idCarpeta, pagina, busqueda],
    queryFn: () => getItemsFolderService(idCarpeta.value, pagina.value, limite, busqueda.value),
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

export function useGetFolderTrashItems(
  idCarpeta: ComputedRef<string>,
  pagina: Ref<number>,
  limite: number = 25,
) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['itemsCarpetaPapelera', authStore.usuario?.id, idCarpeta, pagina],
    queryFn: () => getItemsFolderTrashService(idCarpeta.value, pagina.value, limite),
    enabled: computed(() => !!authStore.usuario?.id && !!idCarpeta.value),
  })
}

export function useGetReceivedItems(pagina: Ref<number>, limite: number = 25) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['itemsRecibidos', authStore.usuario?.id, pagina],
    queryFn: () => getReceivedItemsService(pagina.value, limite),
    enabled: !!authStore.usuario?.id,
  })
}

export function useGetSentItems(pagina: Ref<number>, limite: number = 25) {
  const authStore = useAuthStore()

  return useQuery({
    queryKey: ['itemsCompartidos', authStore.usuario?.id, pagina],
    queryFn: () => getSentItemsService(pagina.value, limite),
    enabled: !!authStore.usuario?.id,
  })
}
