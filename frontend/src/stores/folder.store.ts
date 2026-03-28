import { useLocalStorage } from '@vueuse/core'
import { defineStore } from 'pinia'
import { computed } from 'vue'

interface Carpeta {
  id: string
  nombre: string
}

export const useFolderStore = defineStore('carpetas', () => {
  const carpetaActiva = useLocalStorage<Carpeta[]>('carpeta-activa', [])

  const hayCarpeta = computed(() => !!carpetaActiva.value)

  function setCarpetaActiva(id: string, nombre: string) {
    const index = carpetaActiva.value.findIndex((carpeta) => carpeta.id === id)

    //Si la carpeta ya existe, volvió atrás y cortamos el array hasta la posición
    if (index !== -1) {
      carpetaActiva.value = carpetaActiva.value.slice(0, index + 1)
    } else {
      carpetaActiva.value.push({ id, nombre })
    }
  }

  function limpiarCarpetas() {
    carpetaActiva.value = []
  }

  return { carpetaActiva, hayCarpeta, setCarpetaActiva, limpiarCarpetas }
})
