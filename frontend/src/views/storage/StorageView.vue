<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { useGetFilesUser, useInsertFiles, useMoveFileTrash } from '@/queries/useFilesQuery'
import {
  downloadFileService,
  formatDateService,
  formatearTamañoService,
} from '@/services/file.services'
import {
  Download,
  Ellipsis,
  Folder,
  FolderPlus,
  Plus,
  Share2,
  Trash2,
  Upload,
} from 'lucide-vue-next'
import { computed, defineAsyncComponent, ref } from 'vue'
import { useCreateFolder, useGetFoldersUser, useMoveFolderTrash } from '@/queries/useFoldersQuery'
import getIconExtension from '@/utils/iconMap'
import { useRouter } from 'vue-router'
import { useFolderStore } from '@/stores/folder.store'
import { useShareFolder } from '@/queries/useSharedFoldersQuery'
import { toast } from 'vue-sonner'
import { useShareFile } from '@/queries/useSharedFilesQuery'
import { downloadFolderService } from '@/services/folder.services'

const ArchivoDialog = defineAsyncComponent(() => import('@/components/files/ArchivoDialog.vue'))
const CrearCarpetaDialog = defineAsyncComponent(
  () => import('@/components/folders/CrearCarpetaDialog.vue'),
)
const CompartirCarpetaDialog = defineAsyncComponent(
  () => import('@/components/folders/CompartirCarpetaDialog.vue'),
)
const CompartirArchivoDialog = defineAsyncComponent(
  () => import('@/components/files/CompartirArchivoDialog.vue'),
)

const router = useRouter()
const folderStore = useFolderStore()

const { data: dataFolders, isLoading: loadingFolders } = useGetFoldersUser()
const { data: dataFiles, isLoading: loadingFiles } = useGetFilesUser()
const mutacionInsertar = useInsertFiles()
const { mutateAsync: mutateArchivoPapelera } = useMoveFileTrash()
const { mutateAsync: mutateCarpetaPapelera } = useMoveFolderTrash()
const {
  mutateAsync: mutateCreate,
  isSuccess: successCreate,
  isPending: pendingCreate,
} = useCreateFolder()
const {
  mutateAsync: mutateCompartirCarpeta,
  isSuccess: successCompartirCarpeta,
  isPending: pendingCompartirCarpeta,
} = useShareFolder()
const {
  mutateAsync: mutateCompartirArchivo,
  isSuccess: successCompartirArchivo,
  isPending: pendingCompartirArchivo,
} = useShareFile()

const cargando = computed(() => {
  if (loadingFiles.value || loadingFolders.value) {
    return true
  }

  return false
})

const noData = computed(() => {
  if (
    (!dataFiles.value || dataFiles.value.length < 1) &&
    (!dataFolders.value || dataFolders.value.length < 1)
  ) {
    return true
  }

  return false
})

const subirAbierto = ref<boolean>(false)
const crearAbierto = ref<boolean>(false)
const compartirCarpetaAbierto = ref<boolean>(false)
const idCarpetaSeleccionada = ref<string | null>(null)
const compartirArchivoAbierto = ref<boolean>(false)
const idArchivoSeleccionado = ref<string | null>(null)

async function descargarArchivo(id: string, nombre: string) {
  await downloadFileService(id, nombre)
}

async function crearCarpeta(nombre: string) {
  try {
    await mutateCreate(nombre)
  } catch {}

  if (successCreate) crearAbierto.value = false
}

async function mandarArchivoPapelera(idArchivo: string) {
  try {
    await mutateArchivoPapelera(idArchivo)
  } catch {}
}

async function mandarCarpetaPapelera(idCarpeta: string) {
  try {
    await mutateCarpetaPapelera(idCarpeta)
  } catch {}
}

function handleNavigationDetallesCarpeta(idCarpeta: string, nombreCarpeta: string) {
  folderStore.setCarpetaActiva(idCarpeta, nombreCarpeta)

  router.push({ name: 'carpeta', params: { id: idCarpeta } })
}

async function compartirCarpeta(correo: string) {
  try {
    if (idCarpetaSeleccionada.value) {
      await mutateCompartirCarpeta({
        id_carpeta: idCarpetaSeleccionada.value,
        correo_usuario: correo,
      })

      if (successCompartirCarpeta) compartirCarpetaAbierto.value = false
    } else {
      toast.error('Error al seleccionar la carpeta a compartir')
    }
  } catch {}
}

function abrirCompartirCarpeta(idCarpeta: string) {
  compartirCarpetaAbierto.value = true
  idCarpetaSeleccionada.value = idCarpeta
}

async function compartirArchivo(correo: string) {
  try {
    if (idArchivoSeleccionado.value) {
      await mutateCompartirArchivo({
        id_archivo: idArchivoSeleccionado.value,
        correo_usuario: correo,
      })

      if (successCompartirArchivo) compartirArchivoAbierto.value = false
    } else {
      toast.error('Error al seleccionar el archivo a compartir')
    }
  } catch {}
}

function abrirCompartirArchivo(idArchivo: string) {
  compartirArchivoAbierto.value = true
  idArchivoSeleccionado.value = idArchivo
}

async function descargarCarpeta(id: string, nombre: string) {
  await downloadFolderService(id, nombre)
}
</script>

<template>
  <div class="space-y-2">
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Button variant="outline" class="hover:cursor-pointer">
          <Plus />
          Añadir
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent class="w-56" align="start">
        <DropdownMenuLabel>Archivos</DropdownMenuLabel>
        <DropdownMenuGroup>
          <DropdownMenuItem class="hover:cursor-pointer" @click="subirAbierto = true">
            <Upload />
            Subir archivos
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuLabel>Organización</DropdownMenuLabel>
        <DropdownMenuGroup>
          <DropdownMenuItem class="hover:cursor-pointer" @click="crearAbierto = true">
            <FolderPlus />
            Crear carpeta
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>

    <ArchivoDialog v-model:open="subirAbierto" :subir="mutacionInsertar.mutateAsync" />
    <CompartirArchivoDialog
      v-model:open="compartirArchivoAbierto"
      :pending="pendingCompartirArchivo"
      :reset="compartirArchivoAbierto"
      @compartir-archivo="compartirArchivo"
    />
    <CrearCarpetaDialog
      v-model:open="crearAbierto"
      @crear-carpeta="crearCarpeta"
      :pending="pendingCreate"
      :reset="crearAbierto"
    />
    <CompartirCarpetaDialog
      v-model:open="compartirCarpetaAbierto"
      :pending="pendingCompartirCarpeta"
      :reset="compartirCarpetaAbierto"
      @compartir-carpeta="compartirCarpeta"
    />

    <Table>
      <TableCaption v-if="cargando || noData">
        {{ cargando ? 'Cargando...' : 'Los archivos y carpetas que subas se mostrarán aquí.' }}
      </TableCaption>

      <TableHeader class="bg-neutral-100">
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Subida</TableHead>
          <TableHead>Acciones</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody v-if="!noData">
        <!-- Carpetas -->
        <TableRow
          v-for="folder in dataFolders"
          :key="folder.id"
          @click="handleNavigationDetallesCarpeta(folder.id, folder.nombre_original)"
          class="hover:cursor-pointer"
        >
          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <Folder :size="20" />
              {{ folder.nombre_original }}
            </div>
          </TableCell>
          <TableCell class="font-medium">
            {{ folder.nombre_usuario }}
          </TableCell>
          <TableCell class="font-medium"> - </TableCell>
          <TableCell class="font-medium">
            {{ formatDateService(folder.fecha_creacion) }}
          </TableCell>
          <TableCell>
            <DropdownMenu>
              <DropdownMenuTrigger as-child>
                <Button variant="outline" size="icon" class="hover:cursor-pointer" @click.stop>
                  <Ellipsis />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuLabel>Acciones</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="descargarCarpeta(folder.id, folder.nombre_original)"
                >
                  <Download />
                  Descargar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="mandarCarpetaPapelera(folder.id)"
                >
                  <Trash2 />
                  Eliminar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="abrirCompartirCarpeta(folder.id)"
                >
                  <Share2 />
                  Compartir
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </TableCell>
        </TableRow>

        <!-- Archivos -->
        <TableRow v-for="file in dataFiles" :key="file.id">
          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <component :is="getIconExtension(file.nombre_original)" :size="20" />
              {{ file.nombre_original }}
            </div>
          </TableCell>
          <TableCell class="font-medium">
            {{ file.nombre_usuario }}
          </TableCell>
          <TableCell class="font-medium">
            {{ formatearTamañoService(file.tamaño_bytes) }}
          </TableCell>
          <TableCell class="font-medium">
            {{ formatDateService(file.fecha_creacion) }}
          </TableCell>
          <TableCell>
            <DropdownMenu>
              <DropdownMenuTrigger as-child>
                <Button variant="outline" size="icon" class="hover:cursor-pointer">
                  <Ellipsis />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuLabel>Acciones</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="descargarArchivo(file.id, file.nombre_original)"
                >
                  <Download />
                  Descargar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="mandarArchivoPapelera(file.id)"
                >
                  <Trash2 />
                  Eliminar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="abrirCompartirArchivo(file.id)"
                >
                  <Share2 />
                  Compartir
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
