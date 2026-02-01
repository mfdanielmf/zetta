import type { components } from './backend.types'

// AUTH
export type UserRequest = components['schemas']['UserCreate']
export type UserReturn = components['schemas']['UserReturn']
export type RegisterResponse = components['schemas']['RegisterResponse']
