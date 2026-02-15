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

import { useGetFilesUser } from '@/queries/useFilesQuery';
import { formatDateService, formatearTamañoService } from '@/services/file.services';

const { data } = useGetFilesUser()
</script>

<template>
  <Table>
    <TableCaption v-if="data && data.length < 1">Los archivos que subas se mostrarán aquí.</TableCaption>
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
</template>

