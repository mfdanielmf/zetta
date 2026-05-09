<script setup lang="ts">
import { useDownloadStore } from '@/stores/download.store'
import { useUploadStore } from '@/stores/upload.store'
import DownloadProgress from './DownloadProgress.vue'
import UploadedProgress from './UploadedProgress.vue'

const uploadStore = useUploadStore()
const downloadStore = useDownloadStore()
</script>

<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-4">
    <UploadedProgress v-if="uploadStore.estado" />
    <DownloadProgress v-if="downloadStore.estado" />
  </div>
</template>
