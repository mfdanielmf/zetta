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

import {
  downloadFileService,
  formatDateService,
  formatearTamañoService,
} from '@/services/file.services'
import getIconExtension from '@/utils/iconMap'
import { Download, Ellipsis, Folder, FolderPlus, Plus, Upload } from 'lucide-vue-next'
import { computed, defineAsyncComponent, ref } from 'vue'
import { useRoute } from 'vue-router'

const ArchivoDialog = defineAsyncComponent(() => import('@/components/files/ArchivoDialog.vue'))

const route = useRoute()

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

const { data: dataArchivos, isLoading: loadingArchivos } = useGetFilesFolder(
  route.params.id as string,
)
const { data: dataCarpetasAnidadas, isLoading: loadingCarpetasAnidadas } = useGetFoldersAnidadas(
  route.params.id as string,
)
const mutacionSubir = useUploadFileFolder()
const {
  mutateAsync: mutateCreate,
  isSuccess: successCreate,
  isPending: pendingCreate,
} = useCreateFolderAnidada()

const subirAbierto = ref<boolean>(false)
const crearAbierto = ref<boolean>(false)

async function descargarArchivo(id: string, nombre: string) {
  await downloadFileService(id, nombre)
}

function subirArchivo(formData: FormData) {
  return mutacionSubir.mutateAsync({
    idCarpeta: route.params.id as string,
    data: formData,
  })
}

async function crearCarpeta(nombreCarpeta: string) {
  try {
    await mutateCreate({ idCarpetaPadre: route.params.id as string, nombreCarpeta: nombreCarpeta })
  } catch {}

  if (successCreate) crearAbierto.value = false
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
    <CrearCarpetaDialog
      v-model:open="crearAbierto"
      @crear-carpeta="crearCarpeta"
      :pending="pendingCreate"
      :reset="crearAbierto"
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
