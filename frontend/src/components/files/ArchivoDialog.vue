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
import { computed, ref, useTemplateRef } from 'vue'
import { formatearTamañoService } from '@/services/file.services'
import { X } from 'lucide-vue-next'
import Button from '../ui/button/Button.vue'
import ScrollArea from '../ui/scroll-area/ScrollArea.vue'

const props = defineProps<{
  subir: (formData: FormData) => Promise<unknown>
}>()

type ArchivoType = {
  archivo: File
  invalido: boolean
}

const fileInput = useTemplateRef('fileInput')
const archivos = ref<ArchivoType[]>([])
const TAMAÑO_MAXIMO = 1024 * 1024 * 1024 // 1GB de momento (ya lo sincronizaré con el back en otro momento)

const hayErrores = computed(() => {
  if (archivos.value.some((f) => f.invalido) || archivos.value.length < 1) {
    return true
  }

  return false
})

function handleChange(e: Event) {
  const target = e.target as HTMLInputElement
  const files = target.files as FileList

  const arrayArchivos = Array.from(files)

  archivos.value = arrayArchivos.map((file) => ({
    archivo: file,
    invalido: file.size > TAMAÑO_MAXIMO,
  }))
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
  if (hayErrores.value) return
  if (!archivos.value || archivos.value.length < 1) return

  const formData = new FormData()
  archivos.value.forEach((archivo) => formData.append('file_upload', archivo.archivo))

  //Catch vacío porque ya lo controla el onError de la mutación
  //Para que no salte warning en consola
  try {
    await props.subir(formData)
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
              v-for="(item, index) of archivos"
              :key="item.archivo.name + '-' + item.archivo.lastModified"
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
                <p :class="{ 'text-red-500 font-medium': item.invalido }">
                  {{ item.archivo.name }}
                </p>
                <p :class="{ 'text-red-500': item.invalido }">
                  {{ formatearTamañoService(item.archivo.size) }}
                </p>
                <p v-if="item.invalido" class="text-xs text-red-500">Excede el límite de 1GB</p>
              </div>
            </div>
          </ScrollArea>
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel class="hover:cursor-pointer" @click="eliminarArchivo()">
          Cancelar
        </AlertDialogCancel>
        <AlertDialogAction as-child>
          <Button class="hover:cursor-pointer" @click="subirArchivo" :disabled="hayErrores">
            Continuar
          </Button>
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
