import type { ItemMultipleRequest } from '@/api/types/types'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useSelectedStore = defineStore('selectedStore', () => {
  const itemsSeleccionados = ref<ItemMultipleRequest>([])
  const hayItems = computed(() => itemsSeleccionados.value.length > 0)
  const numItems = computed(() => itemsSeleccionados.value.length)

  function estaSeleccionado(id: string) {
    return itemsSeleccionados.value.some((i) => i.id === id)
  }

  function toggleSeleccionado(id: string, tipo: 'file' | 'folder') {
    const index = itemsSeleccionados.value.findIndex((i) => i.id === id)

    if (index === -1) {
      itemsSeleccionados.value.push({
        id: id,
        tipo: tipo === 'file' ? 'archivo' : 'carpeta',
      })
    } else {
      itemsSeleccionados.value.splice(index, 1)
    }
  }

  function seleccionarTodos(items: ItemMultipleRequest) {
    itemsSeleccionados.value = items
  }

  function reset() {
    itemsSeleccionados.value = []
  }

  return {
    itemsSeleccionados,
    hayItems,
    numItems,
    estaSeleccionado,
    toggleSeleccionado,
    seleccionarTodos,
    reset,
  }
})
