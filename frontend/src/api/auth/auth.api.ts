import api from '../axios.config'
import type { UserRequest, RegisterResponse, LoginRequest, LoginResponse, MeResponse, LogoutResponse } from '../types/types'

export default {
  registrarUsuario(data: UserRequest) {
    return api().post<RegisterResponse>('/auth/register', data)
  },
  iniciarSesion(data: LoginRequest){
    return api().post<LoginResponse>('/auth/login', data)
  },
  obtenerUsuario(){
    return api().get<MeResponse>('/auth/me')
  },
  cerrarSesion(){
    return api().post<LogoutResponse>('/auth/logout')
  }
}
