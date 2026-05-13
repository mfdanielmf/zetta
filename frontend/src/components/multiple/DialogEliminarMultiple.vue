<script setup lang="ts">
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { Trash2 } from 'lucide-vue-next'
import AlertDialogCancel from '../ui/alert-dialog/AlertDialogCancel.vue'
import Spinner from '../ui/spinner/Spinner.vue'

const props = defineProps<{
  pending: boolean
}>()

const emit = defineEmits(['eliminarPermanente'])
</script>

<template>
  <AlertDialog>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>¿Quieres continuar?</AlertDialogTitle>
        <AlertDialogDescription>
          Esta acción no se puede revertir. Todo se eliminará definitivamente.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel class="hover:cursor-pointer">Cancelar</AlertDialogCancel>

        <Button
          class="hover:cursor-pointer bg-red-600 hover:bg-red-700"
          @click="emit('eliminarPermanente')"
          :disabled="props.pending"
        >
          <Spinner v-if="props.pending" />
          <Trash2 v-else />
          {{ props.pending ? 'Eliminando...' : 'Eliminar' }}
        </Button>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
