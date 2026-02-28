import foldersApi from '@/api/folders/folders.api'

export async function crearCarpetasService(nombre: string) {
  const req = await foldersApi.crearCarpeta(nombre)

  return req.data
}
