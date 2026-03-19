import { useLocalStorage } from '@vueuse/core'
import { defineStore } from 'pinia'
import { computed } from 'vue'

export const useFolderStore = defineStore('carpetas', () => {
  const carpetaActiva = useLocalStorage<{
    id: string
    nombre: string
  }>('carpeta-activa', { id: '', nombre: '' })
  const hayCarpeta = computed(() => !!carpetaActiva.value)

  function setCarpetaActiva(id: string, nombre: string) {
    carpetaActiva.value = { id: id, nombre: nombre }
  }

  function limpiarCarpeta() {
    carpetaActiva.value = { id: '', nombre: '' }
  }

  return { carpetaActiva, hayCarpeta, setCarpetaActiva, limpiarCarpeta }
})
