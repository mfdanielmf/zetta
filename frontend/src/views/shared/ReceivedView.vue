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
import { useGetReceivedFiles } from '@/queries/useSharedFilesQuery'
import { useGetReceivedFolders } from '@/queries/useSharedFoldersQuery'

import { formatDateService, formatearTamañoService } from '@/services/file.services'
import { useFolderStore } from '@/stores/folder.store'
import getIconExtension from '@/utils/iconMap'
import { Folder } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const folderStore = useFolderStore()

const cargando = computed(() => {
  if (loadingArchivos.value || loadingCarpetasAnidadas.value) {
    return true
  }

  return false
})

const noData = computed(() => {
  if (
    (!dataArchivos.value || dataArchivos.value?.length < 1) &&
    (!dataCarpetas.value || dataCarpetas.value?.length < 1)
  ) {
    return true
  }

  return false
})

const { data: dataArchivos, isLoading: loadingArchivos } = useGetReceivedFiles()
const { data: dataCarpetas, isLoading: loadingCarpetasAnidadas } = useGetReceivedFolders()

function handleNavigationDetallesCarpeta(idCarpeta: string, nombreCarpeta: string) {
  folderStore.setCarpetaActiva(idCarpeta, nombreCarpeta)

  router.push({ name: 'carpetaRecibida', params: { id: idCarpeta } })
}
</script>

<template>
  <div class="space-y-2">
    <Table>
      <TableCaption v-if="cargando || noData">
        {{
          cargando
            ? 'Cargando...'
            : 'Los archivos y carpetas que compartan contigo se mostrarán aquí.'
        }}
      </TableCaption>

      <TableHeader class="bg-neutral-100">
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Compartido</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody v-if="!noData">
        <!-- Carpetas -->
        <TableRow
          v-for="folder in dataCarpetas"
          :key="folder.id"
          class="hover:cursor-pointer h-13.25"
          @click="
            handleNavigationDetallesCarpeta(folder.carpeta.id, folder.carpeta.nombre_original)
          "
        >
          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <Folder :size="20" />
              {{ folder.carpeta.nombre_original }}
            </div>
          </TableCell>
          <TableCell class="font-medium">
            {{ folder.carpeta.nombre_usuario }}
          </TableCell>
          <TableCell class="font-medium"> - </TableCell>
          <TableCell class="font-medium">
            {{ formatDateService(folder.fecha_compartido) }}
          </TableCell>
        </TableRow>

        <!-- Archivos -->
        <TableRow v-for="file in dataArchivos" :key="file.id" class="h-13.25">
          <TableCell class="font-medium">
            <div class="flex items-center gap-2">
              <component :is="getIconExtension(file.archivo.nombre_original)" :size="20" />
              {{ file.archivo.nombre_original }}
            </div>
          </TableCell>
          <TableCell class="font-medium">
            {{ file.propietario.nombre }}
          </TableCell>
          <TableCell class="font-medium">
            {{ formatearTamañoService(file.archivo.tamaño_bytes) }}
          </TableCell>
          <TableCell class="font-medium">
            {{ formatDateService(file.fecha_compartido) }}
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
