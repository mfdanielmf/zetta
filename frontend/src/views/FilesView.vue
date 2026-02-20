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
import { Plus } from 'lucide-vue-next'
import { ref } from 'vue'

const { data } = useGetFilesUser()

const archivosSubir = ref<File | null>(null)

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const files = target.files

  if (files && files.length > 0) {
    archivosSubir.value = files[0] || null
  }
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
          <DropdownMenuItem as-child @select.prevent>
            <label for="subir-archivo" class="w-full h-full hover:cursor-pointer"
              >Subir archivo</label
            >
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuLabel>Organización</DropdownMenuLabel>
        <DropdownMenuGroup>
          <DropdownMenuItem class="hover:cursor-pointer">Crear carpeta</DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>

    <input type="file" name="subir-archivo" id="subir-archivo" class="hidden" @change="onChange" />

    <Table>
      <TableCaption v-if="data && data.length < 1"
        >Los archivos que subas se mostrarán aquí.</TableCaption
      >

      <TableHeader class="bg-neutral-100">
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Propietario</TableHead>
          <TableHead>Tamaño</TableHead>
          <TableHead>Fecha Creación</TableHead>
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
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
