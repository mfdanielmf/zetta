import api from '../axios.config'
import type { UserRequest, UserReturn } from '../types/types'

export default {
  registrarUsuario(data: UserRequest) {
    return api().post<UserReturn>('/auth/register', data)
  },
}
