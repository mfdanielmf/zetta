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
import ScrollArea from '../ui/scroll-area/ScrollArea.vue'
import type { UseMutationReturnType } from '@tanstack/vue-query'

const props = defineProps<{
  subir: UseMutationReturnType<unknown, unknown, FormData, unknown>
}>()

const fileInput = useTemplateRef('fileInput')
const archivos = ref<File[]>([])

function handleChange(e: Event) {
  const target = e.target as HTMLInputElement
  const files = target.files as FileList

  archivos.value = Array.from(files)
}

function eliminarArchivo(indice: number | null = null) {
  //Eliminamos todos si cerramos el dialog
  if (indice == null) {
    archivos.value = []
    reiniciarInputArchivos()

    return
  }

  archivos.value.splice(indice, 1)
  reiniciarInputArchivos()
}

async function subirArchivo() {
  if (!archivos.value || archivos.value.length < 1) return

  const formData = new FormData()
  archivos.value.forEach((archivo) => formData.append('file_upload', archivo))

  //Catch vacío porque ya lo controla el onError de la mutación
  //Para que no salte warning en consola
  try {
    await props.subir.mutateAsync(formData)
    eliminarArchivo()
  } catch {}
}

function reiniciarInputArchivos() {
  const input = fileInput.value?.$el as HTMLInputElement
  if (input) {
    input.value = ''
  }
}
</script>

<template>
  <AlertDialog>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Añade archivos</AlertDialogTitle>
        <AlertDialogDescription>
          <Input type="file" multiple ref="fileInput" @change="handleChange" />

          <ScrollArea class="h-50 w-full mt-4">
            <div
              class="flex items-center gap-3 mt-4"
              v-for="(archivo, index) of archivos"
              :key="archivo.name + '-' + archivo.lastModified"
            >
              <Button
                variant="outline"
                size="icon-sm"
                class="rounded-full hover:cursor-pointer"
                @click="eliminarArchivo(index)"
              >
                <X />
              </Button>

              <div>
                <p>{{ archivo.name }}</p>
                <p>{{ formatearTamañoService(archivo.size) }}</p>
              </div>
            </div>
          </ScrollArea>
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel class="hover:cursor-pointer" @click="eliminarArchivo()"
          >Cancelar</AlertDialogCancel
        >
        <AlertDialogAction class="hover:cursor-pointer" @click="subirArchivo"
          >Continuar</AlertDialogAction
        >
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
