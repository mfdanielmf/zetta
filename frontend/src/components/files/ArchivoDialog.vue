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
import { ref, useTemplateRef } from 'vue'
import { formatearTamañoService } from '@/services/file.services'
import { X } from 'lucide-vue-next'
import Button from '../ui/button/Button.vue'
import { useInsertFiles } from '@/queries/useFilesQuery'

const fileInput = useTemplateRef('fileInput')
const archivos = ref<File | null | undefined>(null)

const { mutateAsync, isSuccess } = useInsertFiles()

function handleChange(e: Event) {
  const target = e.target as HTMLInputElement
  const files = target.files

  archivos.value = files?.[0]
}

function eliminarArchivo() {
  archivos.value = null

  const input = fileInput.value?.$el as HTMLInputElement
  if (input) {
    input.value = ''
  }
}

async function subirArchivo() {
  if (!archivos.value) return

  const formData = new FormData()
  formData.append('file_upload', archivos.value)

  await mutateAsync(formData)

  if (isSuccess) {
    eliminarArchivo()
  }
}
</script>

<template>
  <AlertDialog>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Añade un archivo</AlertDialogTitle>
        <AlertDialogDescription>
          <Input type="file" ref="fileInput" @change="handleChange" />

          <div v-if="archivos" class="flex items-center gap-3 mt-4">
            <Button
              variant="outline"
              size="icon-sm"
              class="rounded-full hover:cursor-pointer"
              @click="eliminarArchivo"
            >
              <X />
            </Button>
            <div>
              <p>{{ archivos.name }}</p>
              <p>{{ formatearTamañoService(archivos.size) }}</p>
            </div>
          </div>
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel class="hover:cursor-pointer" @click="eliminarArchivo"
          >Cancelar</AlertDialogCancel
        >
        <AlertDialogAction class="hover:cursor-pointer" @click="subirArchivo"
          >Continuar</AlertDialogAction
        >
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
