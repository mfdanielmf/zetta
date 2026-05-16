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
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationFirst,
  PaginationItem,
  PaginationLast,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

import { useDeleteFilePermanent, useRestoreFile } from '@/queries/useFilesQuery'
import { formatDateService, formatearTamañoService } from '@/services/file.services'
import { Ellipsis, Folder, RefreshCcw, SearchIcon, Trash2 } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'
import { useDeleteFolderPermanent, useRestoreFolder } from '@/queries/useFoldersQuery'
import getIconExtension from '@/utils/iconMap'
import { useRouter } from 'vue-router'
import { useFolderStore } from '@/stores/folder.store'
import DialogEliminarArchivo from '@/components/files/DialogEliminarArchivo.vue'
import DialogEliminarCarpeta from '@/components/folders/DialogEliminarCarpeta.vue'
import DialogEliminarMultiple from '@/components/multiple/DialogEliminarMultiple.vue'
import { useGetItemsPapelera } from '@/queries/useItemsQuery'
import { useSelectedStore } from '@/stores/selected.store'
import Checkbox from '@/components/ui/checkbox/Checkbox.vue'
import { useDeleteMultiplePermanent, useRestoreMultiple } from '@/queries/useMultipleQuery'
import { toast } from 'vue-sonner'
import Spinner from '@/components/ui/spinner/Spinner.vue'
import { useDebounceFn } from '@vueuse/core'
import { InputGroup, InputGroupAddon, InputGroupInput } from '@/components/ui/input-group'

const router = useRouter()
const folderStore = useFolderStore()
const selectedStore = useSelectedStore()

const eliminarArchivoAbierto = ref<boolean>(false)
const eliminarCarpetaAbierto = ref<boolean>(false)
const eliminarMultipleAbierto = ref<boolean>(false)
const idEliminar = ref<string>('')
const pagina = ref<number>(1)
const limite = 25
const busqueda = ref<string>('')
const busquedaDebounced = ref<string>('')
const setBusquedaDebounced = useDebounceFn((value: string) => {
  busquedaDebounced.value = value
  pagina.value = 1
}, 500)

watch(busqueda, (nuevoValor: string) => {
  setBusquedaDebounced(nuevoValor)
  selectedStore.reset()
})

const { mutateAsync: mutateRestoreFile } = useRestoreFile()
const { mutateAsync: mutateRestoreFolder } = useRestoreFolder()
const {
  mutateAsync: mutateDeleteFilePermanent,
  isPending: pendingDeleteFile,
  isSuccess: successDeleteFile,
} = useDeleteFilePermanent()
const {
  mutateAsync: mutateDeleteFolderPermanent,
  isPending: pendingDeleteFolder,
  isSuccess: successDeleteFolder,
} = useDeleteFolderPermanent()
const {
  mutateAsync: mutateDeleteMultiple,
  isPending: pendingDeleteMultiple,
  isSuccess: successDeleteMultiple,
} = useDeleteMultiplePermanent()
const {
  mutateAsync: mutateRestoreMultiple,
  isPending: pendingRestoreMultiple,
  isSuccess: successRestoreMultiple,
} = useRestoreMultiple()

const { data: dataItems, isLoading: loadingItems } = useGetItemsPapelera(
  pagina,
  limite,
  busquedaDebounced,
)

const noData = computed(() => {
  if (!dataItems.value || dataItems.value.total < 1) {
    return true
  }

  return false
})

function handleOpenDialogArchivo(id: string) {
  idEliminar.value = id
  eliminarArchivoAbierto.value = true
}

function handleOpenDialogCarpeta(id: string) {
  idEliminar.value = id
  eliminarCarpetaAbierto.value = true
}

function handleNavigationDetallesCarpeta(idCarpeta: string, nombreCarpeta: string) {
  folderStore.setCarpetaActiva(idCarpeta, nombreCarpeta)

  router.push({ name: 'carpetaPapelera', params: { id: idCarpeta } })
}

async function restaurarArchivo(idArchivo: string) {
  try {
    await mutateRestoreFile(idArchivo)
  } catch {}
}

async function restaurarCarpeta(idCarpeta: string) {
  try {
    await mutateRestoreFolder(idCarpeta)
  } catch {}
}

async function eliminarArchivoPermanente(idArchivo: string) {
  try {
    await mutateDeleteFilePermanent(idArchivo)

    if (successDeleteFile) eliminarArchivoAbierto.value = false
  } catch {}
}

async function eliminarCarpetaPermanente(idCarpeta: string) {
  try {
    await mutateDeleteFolderPermanent(idCarpeta)

    if (successDeleteFolder) eliminarCarpetaAbierto.value = false
  } catch {}
}

function handleSelection(id: string, tipo: 'file' | 'folder') {
  selectedStore.toggleSeleccionado(id, tipo)
}

const todosSeleccionados = computed(() => {
  return (
    dataItems &&
    dataItems.value?.items &&
    dataItems.value.items.length > 0 &&
    selectedStore.itemsSeleccionados.length === dataItems.value.items.length
  )
})

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

async function eliminarSeleccionPermanente() {
  try {
    if (selectedStore.hayItems) {
      await mutateDeleteMultiple(selectedStore.itemsSeleccionados)

      if (successDeleteMultiple) {
        selectedStore.reset()
        eliminarMultipleAbierto.value = false
      }
    } else {
      toast.error('Selecciona items')
    }
  } catch {}
}

async function restaurarSeleccion() {
  try {
    if (selectedStore.hayItems) {
      await mutateRestoreMultiple(selectedStore.itemsSeleccionados)

      if (successRestoreMultiple) selectedStore.reset()
    } else {
      toast.error('Selecciona items')
    }
  } catch {}
}
</script>

<template>
  <DialogEliminarArchivo
    v-model:open="eliminarArchivoAbierto"
    @eliminar-permanente="eliminarArchivoPermanente(idEliminar)"
    :pending="pendingDeleteFile"
  />
  <DialogEliminarCarpeta
    v-model:open="eliminarCarpetaAbierto"
    @eliminar-permanente="eliminarCarpetaPermanente(idEliminar)"
    :pending="pendingDeleteFolder"
  />
  <DialogEliminarMultiple
    v-model:open="eliminarMultipleAbierto"
    @eliminar-permanente="eliminarSeleccionPermanente"
    :pending="pendingDeleteFolder"
  />

  <div class="space-y-2">
    <div class="flex flex-col gap-4 justify-between sm:flex-row">
      <div>
        <InputGroup>
          <InputGroupInput placeholder="Buscar..." v-model="busqueda" id="busqueda" />
          <InputGroupAddon>
            <SearchIcon />
          </InputGroupAddon>
          <InputGroupAddon align="inline-end">
            <Spinner v-if="loadingItems" />
            <span v-else>
              {{ dataItems?.total ?? 0 }}
              {{ (dataItems?.total ?? 0) === 1 ? 'resultado' : 'resultados' }}</span
            >
          </InputGroupAddon>
        </InputGroup>
      </div>

      <div class="space-x-4" v-if="selectedStore.hayItems">
        <Button
          variant="outline"
          class="cursor-pointer"
          @click="restaurarSeleccion"
          :disabled="pendingRestoreMultiple"
        >
          <Spinner v-if="pendingRestoreMultiple" />
          <RefreshCcw v-else />
          {{ pendingRestoreMultiple ? 'Restaurando...' : 'Restaurar' }}
        </Button>

        <Button
          class="hover:cursor-pointer bg-red-600 hover:bg-red-700"
          @click="eliminarMultipleAbierto = true"
          :disabled="pendingDeleteMultiple"
        >
          <Spinner v-if="pendingDeleteMultiple" />
          <Trash2 v-else />
          {{ pendingDeleteMultiple ? 'Eliminando...' : 'Eliminar' }}
        </Button>
      </div>
    </div>

    <Table>
      <TableCaption v-if="loadingItems || noData">
        {{
          loadingItems
            ? 'Cargando...'
            : 'Los archivos y carpetas que mandes a la papelera se mostrarán aquí.'
        }}
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
          <TableHead>Fecha Eliminación</TableHead>
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
            {{ item.fecha_eliminacion ? formatDateService(item.fecha_eliminacion) : '-' }}
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
                    item.tipo === 'folder' ? restaurarCarpeta(item.id) : restaurarArchivo(item.id)
                  "
                >
                  <RefreshCcw />
                  Restaurar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="
                    item.tipo === 'folder'
                      ? handleOpenDialogCarpeta(item.id)
                      : handleOpenDialogArchivo(item.id)
                  "
                >
                  <Trash2 />
                  Eliminar definitivamente
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
