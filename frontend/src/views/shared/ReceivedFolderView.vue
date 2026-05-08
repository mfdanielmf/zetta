<script setup lang="ts">
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
import { useGetFolderItems } from '@/queries/useItemsQuery'

import {
  downloadFileService,
  formatDateService,
  formatearTamañoService,
} from '@/services/file.services'
import { downloadFolderService } from '@/services/folder.services'
import { useFolderStore } from '@/stores/folder.store'
import getIconExtension from '@/utils/iconMap'
import { Download, Ellipsis, Folder } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

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

const { data: dataItems, isLoading: loadingItems } = useGetFolderItems(idCarpeta, pagina, limite)

async function descargarArchivo(id: string, nombre: string) {
  await downloadFileService(id, nombre)
}

function handleNavigationDetallesCarpeta(idCarpeta: string, nombreCarpeta: string) {
  folderStore.setCarpetaActiva(idCarpeta, nombreCarpeta)

  router.push({ name: 'carpetaRecibida', params: { id: idCarpeta } })
}

async function descargarCarpeta(id: string, nombre: string) {
  await downloadFolderService(id, nombre)
}
</script>

<template>
  <div class="space-y-2">
    <Table>
      <TableCaption v-if="loadingItems || noData">
        {{ loadingItems ? 'Cargando...' : 'Esta carpeta no tiene contenido' }}
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
