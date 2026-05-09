import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDownloadStore = defineStore('downloadStore', () => {
  const estado = ref<null | 'descargando' | 'completado' | 'error'>(null)
  const porcentaje = ref<number>(0)
  const nombreDescarga = ref<string | null>(null)
  const esCarpeta = ref<boolean>(false)

  function reset() {
    estado.value = null
    porcentaje.value = 0
    nombreDescarga.value = null
    esCarpeta.value = false
  }

  function setPorcentaje(descargado: number, total: number) {
    if (!total) {
      porcentaje.value = 0

      return
    }

    porcentaje.value = Math.round((descargado / total) * 100)
  }

  return { estado, porcentaje, nombreDescarga, esCarpeta, reset, setPorcentaje }
})
