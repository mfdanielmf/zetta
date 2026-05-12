import type { ItemMultipleRequest } from '@/api/types/types'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSelectedStore = defineStore('selectedStore', () => {
  const itemsSeleccionados = ref<ItemMultipleRequest>([])

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

  return { itemsSeleccionados, estaSeleccionado, toggleSeleccionado }
})
