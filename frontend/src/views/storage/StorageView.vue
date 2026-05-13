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
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

import { useInsertFiles, useMoveFileTrash } from '@/queries/useFilesQuery'
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
import { useCreateFolder, useMoveFolderTrash } from '@/queries/useFoldersQuery'
import getIconExtension from '@/utils/iconMap'
import { useRouter } from 'vue-router'
import { useFolderStore } from '@/stores/folder.store'
import { useShareFolder } from '@/queries/useSharedFoldersQuery'
import { toast } from 'vue-sonner'
import { useShareFile } from '@/queries/useSharedFilesQuery'
import { downloadFolderService } from '@/services/folder.services'
import { useGetItemsUser } from '@/queries/useItemsQuery'
import PaginationFirst from '@/components/ui/pagination/PaginationFirst.vue'
import PaginationLast from '@/components/ui/pagination/PaginationLast.vue'
import config from '@/config/config'
import Checkbox from '@/components/ui/checkbox/Checkbox.vue'
import { useSelectedStore } from '@/stores/selected.store'
import { useMoveSelectedTrash, useShareMultiple } from '@/queries/useMultipleQuery'
import Spinner from '@/components/ui/spinner/Spinner.vue'
import { downloadMultipleService } from '@/services/multiple.services'
import { useDownloadStore } from '@/stores/download.store'

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
const CompartirMultipleDialog = defineAsyncComponent(
  () => import('@/components/multiple/CompartirMultipleDialog.vue'),
)

const router = useRouter()
const folderStore = useFolderStore()
const selectedStore = useSelectedStore()
const downloadStore = useDownloadStore()

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
const {
  mutateAsync: mutatePapeleraSelected,
  isSuccess: successPapeleraSelected,
  isPending: pendingPapeleraSelected,
} = useMoveSelectedTrash()
const {
  mutateAsync: mutateShareMultiple,
  isSuccess: successShareMultiple,
  isPending: pendingShareMultiple,
} = useShareMultiple()

const pagina = ref<number>(1)
const limite = config.LIMITE_FETCH

const { data: dataItems, isLoading: loadingItems } = useGetItemsUser(pagina, limite)

const noData = computed(() => {
  if (!dataItems.value || dataItems.value.total < 1) {
    return true
  }

  return false
})

const todosSeleccionados = computed(() => {
  return (
    dataItems &&
    dataItems.value?.items &&
    dataItems.value.items.length > 0 &&
    selectedStore.itemsSeleccionados.length === dataItems.value.items.length
  )
})

const descargandoMultiple = computed(() => {
  return downloadStore.estado === 'preparando' || downloadStore.estado === 'descargando'
})

const subirAbierto = ref<boolean>(false)
const crearAbierto = ref<boolean>(false)
const compartirCarpetaAbierto = ref<boolean>(false)
const idCarpetaSeleccionada = ref<string | null>(null)
const compartirArchivoAbierto = ref<boolean>(false)
const idArchivoSeleccionado = ref<string | null>(null)
const compartirMultipleAbierto = ref<boolean>(false)

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

function handleSelection(id: string, tipo: 'file' | 'folder') {
  selectedStore.toggleSeleccionado(id, tipo)
}

async function mandarPapeleraSeleccion() {
  try {
    if (selectedStore.hayItems) {
      await mutatePapeleraSelected(selectedStore.itemsSeleccionados)

      if (successPapeleraSelected) selectedStore.reset()
    } else {
      toast.error('Selecciona items')
    }
  } catch {}
}

function handleSelectAll(checked: boolean | 'indeterminate') {
  if (checked && dataItems.value?.items) {
    const items = dataItems.value.items

    const arr = items?.map((i) => {
      return {
        id: i.id,
        tipo: (i.tipo === 'file' ? 'archivo' : 'carpeta') as 'archivo' | 'carpeta',
      }
    })

    selectedStore.seleccionarTodos(arr)
  } else {
    selectedStore.reset()
  }
}

async function compartirSeleccion(correo: string) {
  try {
    if (selectedStore.hayItems) {
      const data = {
        correo_usuario: correo,
        items: selectedStore.itemsSeleccionados,
      }

      await mutateShareMultiple(data)

      if (successShareMultiple) {
        selectedStore.reset()
        compartirMultipleAbierto.value = false
      }
    } else {
      toast.error('Selecciona items')
    }
  } catch {}
}

async function descargarSeleccion() {
  try {
    if (selectedStore.hayItems) {
      await downloadMultipleService(selectedStore.itemsSeleccionados)
    } else {
      toast.error('Selecciona items')
    }
  } catch {
  } finally {
    selectedStore.reset()
  }
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex gap-4 justify-between">
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

      <div class="flex items-center gap-4" v-if="selectedStore.hayItems">
        <Button
          variant="outline"
          class="cursor-pointer"
          @click="descargarSeleccion"
          :disabled="descargandoMultiple"
        >
          <Spinner v-if="descargandoMultiple" />
          <Download v-else />
          {{ descargandoMultiple ? 'Descargando...' : 'Descargar' }}
        </Button>

        <Button variant="outline" class="cursor-pointer" @click="compartirMultipleAbierto = true">
          <Share2 />
          Compartir
        </Button>

        <Button
          class="hover:cursor-pointer bg-red-600 hover:bg-red-700"
          @click="mandarPapeleraSeleccion"
          :disabled="pendingPapeleraSelected"
        >
          <Spinner v-if="pendingPapeleraSelected" />
          <Trash2 v-else />
          {{ pendingPapeleraSelected ? 'Eliminando...' : 'Eliminar' }}
        </Button>
      </div>
    </div>

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
    <CompartirMultipleDialog
      v-model:open="compartirMultipleAbierto"
      :pending="pendingShareMultiple"
      :reset="compartirMultipleAbierto"
      @compartir-seleccionado="compartirSeleccion"
    />

    <Table>
      <TableCaption v-if="loadingItems || noData">
        {{ loadingItems ? 'Cargando...' : 'Los archivos y carpetas que subas se mostrarán aquí.' }}
      </TableCaption>

      <TableHeader class="bg-neutral-100">
        <TableRow>
          <TableHead>
            <Checkbox
              class="border-neutral-400"
              :model-value="todosSeleccionados"
              @update:model-value="handleSelectAll"
              v-if="dataItems && dataItems.total > 0"
            />
          </TableHead>
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Subida</TableHead>
          <TableHead>Acciones</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody v-if="!noData">
        <TableRow
          v-for="item in dataItems?.items"
          :key="item.id"
          @click="
            item.tipo === 'folder'
              ? handleNavigationDetallesCarpeta(item.id, item.nombre_original)
              : null
          "
          :class="{ 'hover:cursor-pointer': item.tipo === 'folder' }"
        >
          <TableCell class="cursor-default" @click.stop>
            <Checkbox
              class="border-neutral-400"
              :model-value="selectedStore.estaSeleccionado(item.id)"
              @update:model-value="() => handleSelection(item.id, item.tipo)"
            />
          </TableCell>

          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <Folder :size="20" v-if="item.tipo === 'folder'" />
              <component :is="getIconExtension(item.nombre_original)" :size="20" v-else />
              {{ item.nombre_original }}
            </div>
          </TableCell>
          <TableCell class="font-medium">
            {{ item.nombre_usuario }}
          </TableCell>
          <TableCell class="font-medium">
            {{ item.tipo === 'file' ? formatearTamañoService(item.tamaño_bytes) : '-' }}
          </TableCell>
          <TableCell class="font-medium">
            {{ formatDateService(item.fecha_creacion) }}
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
                  @click="
                    item.tipo === 'folder'
                      ? descargarCarpeta(item.id, item.nombre_original)
                      : descargarArchivo(item.id, item.nombre_original)
                  "
                >
                  <Download />
                  Descargar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="
                    item.tipo === 'folder'
                      ? mandarCarpetaPapelera(item.id)
                      : mandarArchivoPapelera(item.id)
                  "
                >
                  <Trash2 />
                  Eliminar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="
                    item.tipo === 'folder'
                      ? abrirCompartirCarpeta(item.id)
                      : abrirCompartirArchivo(item.id)
                  "
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

  <div class="flex flex-col gap-6 pt-10">
    <Pagination
      v-if="dataItems && dataItems.total > 0"
      v-slot="{ page }"
      :items-per-page="dataItems.limite"
      :total="dataItems?.total"
      v-model:page="pagina"
    >
      <PaginationContent v-slot="{ items }">
        <PaginationPrevious class="hover:cursor-pointer" />
        <PaginationFirst class="hover:cursor-pointer" />
        <template v-for="(item, index) in items" :key="index">
          <PaginationItem
            v-if="item.type === 'page'"
            :value="item.value"
            :is-active="item.value === page"
            class="hover:cursor-pointer"
          >
            {{ item.value }}
          </PaginationItem>
        </template>
        <PaginationEllipsis :index="4" />
        <PaginationLast class="hover:cursor-pointer" />
        <PaginationNext class="hover:cursor-pointer" />
      </PaginationContent>
    </Pagination>
  </div>
</template>
