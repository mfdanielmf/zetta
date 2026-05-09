import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUploadStore = defineStore('uploadStore', () => {
  const estado = ref<'subiendo' | 'procesando' | 'completado' | null>(null)
  const porcentaje = ref<number>(0)

  function reset() {
    estado.value = null
    porcentaje.value = 0
  }

  function setPorcentaje(subido: number, total: number) {
    if (!total) {
      porcentaje.value = 0

      return
    }

    porcentaje.value = Math.round((subido / total) * 100)
  }

  return { estado, porcentaje, reset, setPorcentaje }
})
