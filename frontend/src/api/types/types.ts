import type { components } from './backend.types'

// AUTH
export type UserRequest = components['schemas']['UserCreate']
export type UserReturn = components['schemas']['UserReturn']
export type RegisterResponse = components['schemas']['RegisterResponse']
export type LoginRequest = components['schemas']['LoginRequest']
export type LoginResponse = components['schemas']['LoginResponse']
export type MeResponse = components['schemas']['MeResponse']
export type LogoutResponse = components['schemas']['LogoutResponse']

// FILES
export type GetFilesResponse = components['schemas']['FileBase'][]
export type PostFilesResponse = components['schemas']['FileResponse']

// FOLDERS
export type CreateFolderResponse = components["schemas"]["FolderResponse"]
