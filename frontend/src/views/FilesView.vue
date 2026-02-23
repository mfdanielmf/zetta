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

const ArchivoDialog = defineAsyncComponent(() => import('@/components/files/ArchivoDialog.vue'))

const { data } = useGetFilesUser()

const subirAbierto = ref<boolean>(false)

function descargarArchivo(id: string) {
  console.log('test', id)
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
          <DropdownMenuItem @click="subirAbierto = true" class="hover:cursor-pointer">
            <Upload />
            Subir archivos
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuLabel>Organización</DropdownMenuLabel>
        <DropdownMenuGroup>
          <DropdownMenuItem class="hover:cursor-pointer">
            <FolderPlus />
            Crear carpeta
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>

    <ArchivoDialog v-model:open="subirAbierto" />

    <Table>
      <TableCaption v-if="data && data.length < 1"
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

      <TableBody v-if="data && data.length > 0">
        <TableRow v-for="file in data" :key="file.id">
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
                <DropdownMenuItem class="hover:cursor-pointer" @click="descargarArchivo(file.id)">
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
