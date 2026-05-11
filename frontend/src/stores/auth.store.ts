import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import authApi from '@/api/auth/auth.api'
import type { UserReturn, UserRequest, LoginRequest } from '@/api/types/types'
import axios from 'axios'
import { toast } from 'vue-sonner'

export const useAuthStore = defineStore('auth-store', () => {
  const usuario = ref<null | UserReturn>(null)
  const cargando = ref<boolean>(false)
  const obteniendoUsuario = ref<boolean>(false)
  const logueado = computed(() => !!usuario.value)

  async function registrarUsuario(data: UserRequest) {
    cargando.value = true

    try {
      const req = await authApi.registrarUsuario(data)

      toast.success(req.data.msg || 'Usuario registrado correctamente')

      usuario.value = req.data.usuario

      return true //Hacer push a la ruta de login
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Ocurrió un error inesperado al registrarse')
      } else {
        toast.error('Ocurrió un error inesperado al registrarse')
      }

      usuario.value = null

      return false // No hacer push a login
    } finally {
      cargando.value = false
    }
  }

  async function iniciarSesion(data: LoginRequest) {
    cargando.value = true

    try {
      const req = await authApi.iniciarSesion(data)

      localStorage.setItem('tokenZetta', req.data.token)

      usuario.value = req.data.usuario

      toast.success(req.data.msg || 'Sesión iniciada correctamente')

      return true // Hacer push
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        toast.error(e.response?.data?.detail || 'Ocurrió un error inesperado al iniciar sesión')
      } else {
        toast.error('Ocurrió un error inesperado al iniciar sesión')
      }

      usuario.value = null
      localStorage.removeItem('tokenZetta')

      return false // No hacer push
    } finally {
      cargando.value = false
    }
  }

  // Endpoint me
  async function obtenerUsuario() {
    obteniendoUsuario.value = true

    try {
      const req = await authApi.obtenerUsuario()

      usuario.value = req.data.usuario

      return true //Redirigir dash
    } catch {
      usuario.value = null

      return false //Redigir login
    } finally {
      obteniendoUsuario.value = false
    }
  }

  function cerrarSesion() {
    try {
      localStorage.removeItem('tokenZetta')
      usuario.value = null

      toast.success('Sesión cerrada con éxito')

      return true
    } catch {
      toast.error('Ocurrió un error al cerrar sesión')

      return false
    }
  }

  return {
    usuario,
    logueado,
    cargando,
    obteniendoUsuario,
    registrarUsuario,
    iniciarSesion,
    obtenerUsuario,
    cerrarSesion,
  }
})
