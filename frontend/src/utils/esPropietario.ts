import { useAuthStore } from '@/stores/auth.store'

const authStore = useAuthStore()

export default function esPropietario(nombrePropietario: string) {
  return authStore.usuario?.nombre === nombrePropietario
}
