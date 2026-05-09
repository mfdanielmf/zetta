<script lang="ts" setup>
import { Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'
import UploadedProgress from './components/UploadedProgress.vue'
import { useUploadStore } from './stores/upload.store'

const uploadStore = useUploadStore()
</script>

<template>
  <Toaster :close-button="true" position="top-right" />
  <RouterView />
  <UploadedProgress v-if="uploadStore.estado" />
</template>
