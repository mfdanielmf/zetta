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

import { useGetFilesUser } from '@/queries/useFilesQuery'
import { formatDateService, formatearTamañoService } from '@/services/file.services'
import { Download, Ellipsis, FolderPlus, Plus, Upload } from 'lucide-vue-next'
import { defineAsyncComponent, ref } from 'vue'
import filesApi from '@/api/files/files.api'
import { toast } from 'vue-sonner'
import { useCreateFolder } from '@/queries/useFoldersQuery'

const ArchivoDialog = defineAsyncComponent(() => import('@/components/files/ArchivoDialog.vue'))
const CrearCarpetaDialog = defineAsyncComponent(
  () => import('@/components/folders/CrearCarpetaDialog.vue'),
)

const { data: dataFiles } = useGetFilesUser()
const {
  mutateAsync: mutateCreate,
  isSuccess: successCreate,
  isPending: pendingCreate,
} = useCreateFolder()

const subirAbierto = ref<boolean>(false)
const crearAbierto = ref<boolean>(false)

async function descargarArchivo(id: string, nombre: string) {
  try {
    const req = await filesApi.descargarArchivo(id)

    const blob = new Blob([req.data], {
      type: req.headers['content-type'],
    })

    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', nombre)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch {
    toast.error('Ha ocurrido un error al descargar los archivos')
  }
}

async function crearCarpeta(nombre: string) {
  await mutateCreate(nombre)

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

    <ArchivoDialog v-model:open="subirAbierto" />
    <CrearCarpetaDialog
      v-model:open="crearAbierto"
      @crear-carpeta="crearCarpeta"
      :pending="pendingCreate"
    />

    <Table>
      <TableCaption v-if="dataFiles && dataFiles.length < 1"
        >Los archivos que subas se mostrarán aquí.</TableCaption
      >

      <TableHeader class="bg-neutral-100">
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Subida</TableHead>
          <TableHead>Acciones</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody v-if="dataFiles && dataFiles.length > 0">
        <TableRow v-for="file in dataFiles" :key="file.id">
          <TableCell class="font-medium">
            {{ file.nombre_original }}
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
