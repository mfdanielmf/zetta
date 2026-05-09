<script setup lang="ts">
import Spinner from '../ui/spinner/Spinner.vue'
import { Check, X } from 'lucide-vue-next'
import Button from '../ui/button/Button.vue'
import { useDownloadStore } from '@/stores/download.store'

const downloadStore = useDownloadStore()

function cerrar() {
  downloadStore.reset()
}
</script>

<template>
  <div class="w-72 bg-white border rounded-xl shadow-sm p-4 z-50">
    <div class="flex justify-between items-center mb-2 gap-2">
      <p class="font-semibold truncate">
        {{ downloadStore.nombreDescarga ? downloadStore.nombreDescarga : 'Descargando 1 elemento' }}
      </p>

      <Button
        class="cursor-pointer rounded-full"
        size="icon-sm"
        aria-label="Submit"
        variant="outline"
        @click="cerrar"
        v-if="downloadStore.estado === 'completado' || downloadStore.estado === 'error'"
      >
        <X />
      </Button>
    </div>

    <div class="text-sm mb-3 text-gray-700">
      <span v-if="downloadStore.estado === 'descargando'" class="flex items-center gap-1">
        <Spinner />
        Descargando...
      </span>

      <span v-else-if="downloadStore.estado === 'completado'" class="flex items-center gap-1">
        <Check :size="18" />
        Completado
      </span>

      <span v-else-if="downloadStore.estado === 'error'" class="flex items-center gap-1">
        <X :size="18" color="red" />
        Error al subir
      </span>
    </div>

    <div
      class="w-full h-2 bg-gray-200 rounded-full overflow-hidden"
      v-if="downloadStore.estado !== 'error'"
    >
      <div
        class="h-full bg-green-500 transition-all duration-200"
        :style="{ width: downloadStore.porcentaje + '%' }"
      />
    </div>

    <p class="text-xs text-right mt-2" v-if="downloadStore.estado !== 'error'">
      {{ downloadStore.porcentaje }}%
    </p>
  </div>
</template>
