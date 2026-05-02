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
import { useGetFilesFolder, useGetFoldersAnidadas } from '@/queries/useFoldersQuery'

import {
  downloadFileService,
  formatDateService,
  formatearTamañoService,
} from '@/services/file.services'
import { downloadFolderService } from '@/services/folder.services'
import { useFolderStore } from '@/stores/folder.store'
import getIconExtension from '@/utils/iconMap'
import { Download, Ellipsis, Folder } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

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
      <TableCaption v-if="cargando || noData">
        {{ cargando ? 'Cargando...' : 'Esta carpeta no tiene contenido' }}
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
                <DropdownMenuItem
                  class="hover:cursor-pointer"
                  @click="descargarCarpeta(folder.id, folder.nombre_original)"
                >
                  <Download />
                  Descargar
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
              </DropdownMenuContent>
            </DropdownMenu>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
