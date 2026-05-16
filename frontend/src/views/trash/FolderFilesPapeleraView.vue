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

import config from '@/config/config'
import { useGetFolderTrashItems } from '@/queries/useItemsQuery'

import { formatDateService, formatearTamañoService } from '@/services/file.services'
import { useFolderStore } from '@/stores/folder.store'
import getIconExtension from '@/utils/iconMap'
import { Folder, SearchIcon } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDebounceFn } from '@vueuse/core'
import { InputGroup, InputGroupAddon, InputGroupInput } from '@/components/ui/input-group'
import Spinner from '@/components/ui/spinner/Spinner.vue'

const route = useRoute()
const router = useRouter()
const folderStore = useFolderStore()

const idCarpeta = computed(() => route.params.id as string)

const noData = computed(() => {
  if (!dataItems.value || dataItems.value.total < 1) {
    return true
  }

  return false
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
})

const { data: dataItems, isLoading: loadingItems } = useGetFolderTrashItems(
  idCarpeta,
  pagina,
  limite,
  busquedaDebounced,
)

function handleNavigationDetallesCarpeta(idCarpeta: string, nombreCarpeta: string) {
  folderStore.setCarpetaActiva(idCarpeta, nombreCarpeta)

  router.push({ name: 'carpetaPapelera', params: { id: idCarpeta } })
}
</script>

<template>
  <div class="space-y-2">
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

    <Table>
      <TableCaption v-if="loadingItems || noData">
        {{ loadingItems ? 'Cargando...' : 'Esta carpeta no tiene contenido.' }}
      </TableCaption>

      <TableHeader class="bg-neutral-100">
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Eliminación</TableHead>
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
          class="h-13.25"
          :class="{ 'hover:cursor-pointer': item.tipo === 'folder' }"
        >
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
