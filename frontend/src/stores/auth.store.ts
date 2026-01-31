import { defineStore } from 'pinia'
import { ref } from 'vue'
import authApi from '@/api/auth/auth.api'
import type { UserReturn, UserRequest } from '@/api/types/types'
import axios from 'axios'
import { toast } from 'vue-sonner'

export const useAuthStore = defineStore('auth-store', () => {
  const usuario = ref<null | UserReturn>(null)
  const logueado = ref<boolean>(false)
  const cargando = ref<boolean>(false)

  async function registrarUsuario(data: UserRequest) {
    cargando.value = true

    try {
      const req = await authApi.registrarUsuario(data)

      usuario.value = req.data
      logueado.value = true
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Ocurrió un error inesperado al registrarse', {
          position: 'top-right',
        })
      } else {
        toast.error('Ocurrió un error inesperado al registrarse', {
          position: 'top-right',
        })
      }

      usuario.value = null
      logueado.value = false
    } finally {
      cargando.value = false
    }
  }

  return { registrarUsuario }
})
