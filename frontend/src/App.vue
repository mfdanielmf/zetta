<script lang="ts" setup>
import { Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'
import UploadedProgress from './components/progress/UploadedProgress.vue'
import DownloadProgress from './components/progress/DownloadProgress.vue'
import { useUploadStore } from './stores/upload.store'
import { useDownloadStore } from './stores/download.store'

const uploadStore = useUploadStore()
const downloadStore = useDownloadStore()
</script>

<template>
  <Toaster :close-button="true" position="top-right" />
  <RouterView />
  <UploadedProgress v-if="uploadStore.estado" />
  <DownloadProgress v-if="downloadStore.estado" />
</template>
