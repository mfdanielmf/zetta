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
import { Ellipsis, Folder, RefreshCcw, Trash2 } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useDeleteFolderPermanent, useRestoreFolder } from '@/queries/useFoldersQuery'
import getIconExtension from '@/utils/iconMap'
import { useRouter } from 'vue-router'
import { useFolderStore } from '@/stores/folder.store'
import DialogEliminarArchivo from '@/components/files/DialogEliminarArchivo.vue'
import DialogEliminarCarpeta from '@/components/folders/DialogEliminarCarpeta.vue'
import { useGetItemsPapelera } from '@/queries/useItemsQuery'

const router = useRouter()
const folderStore = useFolderStore()

const eliminarArchivoAbierto = ref<boolean>(false)
const eliminarCarpetaAbierto = ref<boolean>(false)
const idEliminar = ref<string>('')
const pagina = ref<number>(1)
const limite = 25

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

const { data: dataItems, isLoading: loadingItems } = useGetItemsPapelera(pagina, limite)

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

  <div class="space-y-2">
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
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Eliminación</TableHead>
          <TableHead>Acciones</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody v-if="!noData">
        <!-- Carpetas -->
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
