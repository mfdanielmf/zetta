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

      toast.success(req.data.msg || 'Usuario registrado correctamente')

      usuario.value = req.data.usuario
      logueado.value = true

      return true //Hacer push a la ruta de login
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

      return false // No hacer push a login
    } finally {
      cargando.value = false
    }
  }

  return { registrarUsuario }
})
