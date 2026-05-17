<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import Button from '@/components/ui/button/Button.vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import {
  downloadFileService,
  formatDateService,
  formatearTamañoService,
} from '@/services/file.services'

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
import { useFolderStore } from '@/stores/folder.store'
import getIconExtension from '@/utils/iconMap'
import { Download, Ellipsis, Folder, SearchIcon, UserRoundX } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { downloadFolderService } from '@/services/folder.services'
import { useGetSentItems } from '@/queries/useItemsQuery'
import config from '@/config/config'
import { toast } from 'vue-sonner'
import { useSelectedStore } from '@/stores/selected.store'
import { downloadMultipleService } from '@/services/multiple.services'
import Checkbox from '@/components/ui/checkbox/Checkbox.vue'
import Spinner from '@/components/ui/spinner/Spinner.vue'
import { useDownloadStore } from '@/stores/download.store'
import { InputGroup, InputGroupAddon, InputGroupInput } from '@/components/ui/input-group'
import { useDebounceFn } from '@vueuse/core'
import { useCancelMultipleShared } from '@/queries/useMultipleQuery'
import type { ItemMultipleRequest } from '@/api/types/types'

const router = useRouter()
const folderStore = useFolderStore()
const selectedStore = useSelectedStore()
const downloadStore = useDownloadStore()

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

const pagina = ref<number>(1)
const limite = config.LIMITE_FETCH
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

const { data: dataItems, isLoading: loadingItems } = useGetSentItems(
  pagina,
  limite,
  busquedaDebounced,
)

const {
  mutateAsync: mutateCancelarMultiple,
  isPending: pendingCancelarMultiple,
  isSuccess: successCancelarMultiple,
} = useCancelMultipleShared()

function handleNavigationDetallesCarpeta(idCarpeta: string, nombreCarpeta: string) {
  folderStore.setCarpetaActiva(idCarpeta, nombreCarpeta)

  router.push({ name: 'carpetaCompartida', params: { id: idCarpeta } })
}

async function descargarArchivo(id: string, nombre: string) {
  await downloadFileService(id, nombre)
}

async function descargarCarpeta(id: string, nombre: string) {
  await downloadFolderService(id, nombre)
}

function handleSelection(id: string, tipo: 'file' | 'folder') {
  selectedStore.toggleSeleccionado(id, tipo)
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

function handleSelectAll(checked: boolean | 'indeterminate') {
  if (checked && dataItems.value?.items) {
    const items = dataItems.value.items

    const arr = items?.map((i) => {
      return {
        id: i.tipo === 'file' ? i.archivo.id : i.carpeta.id,
        tipo: (i.tipo === 'file' ? 'archivo' : 'carpeta') as 'archivo' | 'carpeta',
        id_compartido: i.id
      }
    })

    selectedStore.seleccionarTodos(arr)
  } else {
    selectedStore.reset()
  }
}

async function cancelarCompartido(idElemento: string, tipo: 'archivo' | 'carpeta', idCompartido: string) {
  try {
    const data: ItemMultipleRequest = [
      {
        id: idElemento,
        tipo: tipo,
        id_compartido: idCompartido
      }
    ]

    await mutateCancelarMultiple(data)
  } catch {}
}

async function cancelarCompartidoSeleccion() {
  try {
    if (selectedStore.hayItems) {
      console.log(selectedStore.itemsSeleccionados);
      await mutateCancelarMultiple(selectedStore.itemsSeleccionados)

      if (successCancelarMultiple) selectedStore.reset()
    } else {
      toast.error('Selecciona items')
    }
  } catch {}
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex items-center justify-between gap-4">
      <InputGroup class="max-w-73.5">
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

      <div class="space-x-4" v-if="selectedStore.hayItems">
        <Button
          variant="outline"
          class="cursor-pointer"
          @click="descargarSeleccion"
          :disabled="downloadStore.descargandoMultiple"
        >
          <Spinner v-if="downloadStore.descargandoMultiple" />
          <Download v-else />
          {{ downloadStore.descargandoMultiple ? 'Descargando...' : 'Descargar' }}
        </Button>

        <Button
          variant="outline"
          class="cursor-pointer"
          @click="cancelarCompartidoSeleccion"
          :disabled="pendingCancelarMultiple"
        >
          <Spinner v-if="pendingCancelarMultiple" />
          <UserRoundX v-else />
          {{ pendingCancelarMultiple ? 'Cancelando...' : 'Cancelar compartido' }}
        </Button>
      </div>
    </div>

    <Table>
      <TableCaption v-if="loadingItems || noData">
        {{
          loadingItems ? 'Cargando...' : 'Los archivos y carpetas que compartas se mostrarán aquí.'
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
          <TableHead>Compartido Con</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Compartido</TableHead>
          <TableHead>Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody v-if="!noData">
        <TableRow
          v-for="item in dataItems?.items"
          :key="item.id"
          @click="
            item.tipo === 'folder'
              ? handleNavigationDetallesCarpeta(item.carpeta.id, item.carpeta.nombre_original)
              : null
          "
          :class="{ 'hover:cursor-pointer': item.tipo === 'folder' }"
        >
          <TableCell class="cursor-default" @click.stop>
            <Checkbox
              class="border-neutral-400"
              :model-value="
                selectedStore.estaSeleccionado(
                  item.tipo === 'file' ? item.archivo.id : item.carpeta.id,
                )
              "
              @update:model-value="
                () =>
                  handleSelection(
                    item.tipo === 'file' ? item.archivo.id : item.carpeta.id,
                    item.tipo,
                  )
              "
            />
          </TableCell>
          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <Folder :size="20" v-if="item.tipo === 'folder'" />
              <component :is="getIconExtension(item.archivo.nombre_original)" :size="20" v-else />
              {{
                item.tipo === 'folder' ? item.carpeta.nombre_original : item.archivo.nombre_original
              }}
            </div>
          </TableCell>
          <TableCell class="font-medium">
            {{ item.propietario.nombre }}
          </TableCell>
          <TableCell class="font-medium">
            {{ item.receptor.nombre }}
          </TableCell>
          <TableCell class="font-medium">
            {{ item.tipo === 'file' ? formatearTamañoService(item.archivo.tamaño_bytes) : '-' }}
          </TableCell>
          <TableCell class="font-medium">
            {{ formatDateService(item.fecha_compartido) }}
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
                  class="cursor-pointer"
                  @click="
                    item.tipo === 'folder'
                      ? descargarCarpeta(item.carpeta.id, item.carpeta.nombre_original)
                      : descargarArchivo(item.archivo.id, item.archivo.nombre_original)
                  "
                >
                  <Download />
                  Descargar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="cursor-pointer"
                  @click="
                    cancelarCompartido(
                      item.tipo === 'file' ? item.archivo.id : item.carpeta.id,
                      item.tipo === 'file' ? 'archivo' : 'carpeta',
                      item.id
                    )
                  "
                >
                  <UserRoundX />
                  Cancelar compartido
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
