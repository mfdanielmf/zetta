<script setup lang="ts">
import { useUploadStore } from '@/stores/upload.store'
import Spinner from './ui/spinner/Spinner.vue'
import { Check } from 'lucide-vue-next'

const uploadStore = useUploadStore()
</script>

<template>
  <div class="fixed bottom-5 right-5 w-72 bg-white rounded-xl shadow-lg p-4 z-50">
    <p class="font-semibold mb-2">Progreso de la subida:</p>

    <div class="text-sm mb-3 text-gray-700">
      <span v-if="uploadStore.estado === 'subiendo'" class="flex items-center gap-2">
        <Spinner />
        Subiendo...
      </span>

      <span v-else-if="uploadStore.estado === 'procesando'" class="flex items-center gap-2">
        <Spinner class="size-18" />
        Procesando subida...
      </span>

      <span v-else-if="uploadStore.estado === 'completado'" class="flex items-center gap-2">
        <Check :size="18" />
        Completado
      </span>
    </div>

    <div class="w-full h-2 rounded-full overflow-hidden">
      <div
        class="h-full bg-green-500 transition-all duration-200"
        :style="{ width: uploadStore.porcentaje + '%' }"
      />
    </div>

    <p class="text-xs text-right mt-2">{{ uploadStore.porcentaje }}%</p>
  </div>
</template>
