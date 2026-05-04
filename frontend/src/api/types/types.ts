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
export type GetFilesResponse = components['schemas']['PaginatedFileResponse']
export type PostFilesResponse = components['schemas']['FileResponse']
export type SendFileTrashResponse = components['schemas']['AddFileTrashResponse']
export type GetFilesTrashResponse = components['schemas']['FileBase'][]
export type RestoreFileResponse = components['schemas']['RestoreFileResponse']
export type DeleteFilePermanentResponse = components['schemas']['DeleteFilePermanentResponse']

// FOLDERS
export type CreateFolderResponse = components['schemas']['FolderResponse']
export type GetFoldersResponse = components['schemas']['PaginatedFolderResponse']
export type GetFilesFolderResponse = components['schemas']['PaginatedFileResponse']
export type UploadFileFolderResponse = components['schemas']['UploadFileFolderResponse']
export type CreateFolderAnidadaResponse = components['schemas']['FolderResponse']
export type GetFoldersAnidada = components['schemas']['PaginatedFolderResponse']
export type SendFolderTrashResponse = components['schemas']['AddFolderTrashResponse']
export type GetFoldersTrashResponse = components['schemas']['FolderBase'][]
export type RestoreFolderResponse = components['schemas']['RestoreFolderResponse']
export type DeleteFolderPermanentResponse = components['schemas']['DeleteFolderPermanentResponse']
export type GetFilesFolderTrashResponse = components['schemas']['FileBase'][]
export type GetFoldersAnidadaTrashResponse = components['schemas']['FolderBase'][]

// SHARED
export type GetSharedFilesByMeResponse = components['schemas']['ArchivoCompartidoBase'][]
export type GetSharedFoldersByMeResponse = components['schemas']['CarpetaCompartidaBase'][]
export type GetReceivedFilesResponse = components['schemas']['ArchivoCompartidoBase'][]
export type ShareFileRequest = components['schemas']['ShareFileRequest']
export type ShareFileResponse = components['schemas']['ShareFileResponse']
export type ShareFolderRequest = components['schemas']['ShareFolderRequest']
export type ShareFolderResponse = components['schemas']['ShareFolderResponse']
export type GetReceivedFoldersResponse = components['schemas']['CarpetaCompartidaBase'][]

//ITEMS
export type GetItemsResponse = components['schemas']['PaginatedItemResponse']
export type GetFolderItemsResponse = components["schemas"]["PaginatedItemResponse"]
export type GetItemsTrashResponse = components["schemas"]["PaginatedItemResponse"]
export type GetItemsFolderTrashResponse = components["schemas"]["PaginatedItemResponse"]
