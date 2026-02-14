<script setup lang="ts">
import Skeleton from '@/components/ui/skeleton/Skeleton.vue';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import { useGetFilesUser } from '@/queries/useFilesQuery';

const { data, isLoading } = useGetFilesUser()
</script>

<template>
  <Table>
    <TableCaption v-if="data && data.length < 1">Los archivos que subas se mostrarán aquí.</TableCaption>
    <TableHeader class="bg-neutral-100">
      <TableRow>
        <TableHead>
          Nombre
        </TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <div v-if="isLoading">
        <Skeleton  v-for="i in 10" :key="i" class="h-4 w-full"/>
      </div>
      <TableRow v-for="file in data" :key="file.id">
        <TableCell class="font-medium">
          {{ file.nombre_original}}
        </TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>

