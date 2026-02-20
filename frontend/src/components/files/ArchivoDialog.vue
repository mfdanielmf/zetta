<script setup lang="ts">
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import Input from '../ui/input/Input.vue'
</script>

<template>
  <AlertDialog>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Añade un archivo</AlertDialogTitle>
        <AlertDialogDescription>
          <Input type="file" />
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel class="hover:cursor-pointer">Cancelar</AlertDialogCancel>
        <AlertDialogAction class="hover:cursor-pointer">Continuar</AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
