import api from '../axios.config'
import type { UserRequest, RegisterResponse } from '../types/types'

export default {
  registrarUsuario(data: UserRequest) {
    return api().post<RegisterResponse>('/auth/register', data)
  },
}
