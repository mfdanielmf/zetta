<script setup lang="ts">
import CrearCarpetaDialog from '@/components/folders/CrearCarpetaDialog.vue'
import Button from '@/components/ui/button/Button.vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import DropdownMenuGroup from '@/components/ui/dropdown-menu/DropdownMenuGroup.vue'
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
  useCreateFolderAnidada,
  useGetFilesFolder,
  useGetFoldersAnidadas,
  useUploadFileFolder,
} from '@/queries/useFoldersQuery'
import { useShareFile } from '@/queries/useSharedFilesQuery'
import { useShareFolder } from '@/queries/useSharedFoldersQuery'

import {
  downloadFileService,
  formatDateService,
  formatearTamañoService,
} from '@/services/file.services'
import { useFolderStore } from '@/stores/folder.store'
import getIconExtension from '@/utils/iconMap'
import { Download, Ellipsis, Folder, FolderPlus, Plus, Share2, Upload } from 'lucide-vue-next'
import { computed, defineAsyncComponent, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const ArchivoDialog = defineAsyncComponent(() => import('@/components/files/ArchivoDialog.vue'))
const CompartirCarpetaDialog = defineAsyncComponent(
  () => import('@/components/folders/CompartirCarpetaDialog.vue'),
)
const CompartirArchivoDialog = defineAsyncComponent(
  () => import('@/components/files/CompartirArchivoDialog.vue'),
)

const route = useRoute()
const router = useRouter()
const folderStore = useFolderStore()

const idCarpeta = computed(() => route.params.id as string)

const cargando = computed(() => {
  if (loadingArchivos.value || loadingCarpetasAnidadas.value) {
    return true
  }

  return false
})

const noData = computed(() => {
  if (
    (!dataArchivos.value || dataArchivos.value?.length < 1) &&
    (!dataCarpetasAnidadas.value || dataCarpetasAnidadas.value?.length < 1)
  ) {
    return true
  }

  return false
})

const { data: dataArchivos, isLoading: loadingArchivos } = useGetFilesFolder(idCarpeta)
const { data: dataCarpetasAnidadas, isLoading: loadingCarpetasAnidadas } =
  useGetFoldersAnidadas(idCarpeta)
const mutacionSubir = useUploadFileFolder()
const {
  mutateAsync: mutateCreate,
  isSuccess: successCreate,
  isPending: pendingCreate,
} = useCreateFolderAnidada()
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

const subirAbierto = ref<boolean>(false)
const crearAbierto = ref<boolean>(false)
const compartirCarpetaAbierto = ref<boolean>(false)
const idCarpetaSeleccionada = ref<string | null>(null)
const compartirArchivoAbierto = ref<boolean>(false)
const idArchivoSeleccionado = ref<string | null>(null)

async function descargarArchivo(id: string, nombre: string) {
  await downloadFileService(id, nombre)
}

function subirArchivo(formData: FormData) {
  return mutacionSubir.mutateAsync({
    idCarpeta: idCarpeta.value,
    data: formData,
  })
}

async function crearCarpeta(nombreCarpeta: string) {
  try {
    await mutateCreate({ idCarpetaPadre: idCarpeta.value, nombreCarpeta: nombreCarpeta })
  } catch {}

  if (successCreate) crearAbierto.value = false
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

    <ArchivoDialog v-model:open="subirAbierto" :subir="subirArchivo" />
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
          v-for="folder in dataCarpetasAnidadas"
          :key="folder.id"
          class="hover:cursor-pointer"
          @click="handleNavigationDetallesCarpeta(folder.id, folder.nombre_original)"
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
                <DropdownMenuItem class="hover:cursor-pointer" @click="console.log('test')">
                  <Download />
                  Descargar
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
        <TableRow v-for="file in dataArchivos" :key="file.id">
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
