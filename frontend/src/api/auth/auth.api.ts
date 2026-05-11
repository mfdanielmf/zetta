import api from '../axios.config'
import type {
  UserRequest,
  RegisterResponse,
  LoginRequest,
  LoginResponse,
  MeResponse,
} from '../types/types'

const URL = '/auth'

export default {
  registrarUsuario(data: UserRequest) {
    return api().post<RegisterResponse>(URL + `/register`, data)
  },
  iniciarSesion(data: LoginRequest) {
    return api().post<LoginResponse>(URL + `/login`, data)
  },
  obtenerUsuario() {
    return api().get<MeResponse>(URL + `/me`)
  },
}
