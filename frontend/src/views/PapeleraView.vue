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

import { useDeleteFilePermanent, useGetFilesTrash, useRestoreFile } from '@/queries/useFilesQuery'
import { formatDateService, formatearTamañoService } from '@/services/file.services'
import { Ellipsis, Folder, RefreshCcw, Trash2 } from 'lucide-vue-next'
import { computed } from 'vue'
import {
  useDeleteFolderPermanent,
  useGetFoldersTrash,
  useRestoreFolder,
} from '@/queries/useFoldersQuery'
import getIconExtension from '@/utils/iconMap'
import { useRouter } from 'vue-router'
import { useFolderStore } from '@/stores/folder.store'

const router = useRouter()
const folderStore = useFolderStore()

const { data: dataFolders, isLoading: loadingFolders } = useGetFoldersTrash()
const { data: dataFiles, isLoading: loadingFiles } = useGetFilesTrash()
const { mutateAsync: mutateRestoreFile } = useRestoreFile()
const { mutateAsync: mutateRestoreFolder } = useRestoreFolder()
const { mutateAsync: mutateDeleteFilePermanent } = useDeleteFilePermanent()
const { mutateAsync: mutateDeleteFolderPermanent } = useDeleteFolderPermanent()

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
  } catch {}
}

async function eliminarCarpetaPermanente(idCarpeta: string) {
  try {
    await mutateDeleteFolderPermanent(idCarpeta)
  } catch {}
}
</script>

<template>
  <div class="space-y-2">
    <Table>
      <TableCaption v-if="cargando || noData">
        {{
          cargando
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
            {{ folder.fecha_eliminacion ? formatDateService(folder.fecha_eliminacion) : '-' }}
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
                <DropdownMenuItem class="hover:cursor-pointer" @click="restaurarCarpeta(folder.id)">
                  <RefreshCcw />
                  Restaurar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="eliminarCarpetaPermanente(folder.id)"
                >
                  <Trash2 />
                  Eliminar definitivamente
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
            {{ file.fecha_eliminacion ? formatDateService(file.fecha_eliminacion) : '-' }}
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
                <DropdownMenuItem class="hover:cursor-pointer" @click="restaurarArchivo(file.id)">
                  <RefreshCcw />
                  Restaurar
                </DropdownMenuItem>
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="eliminarArchivoPermanente(file.id)"
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
</template>
