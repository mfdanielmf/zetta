<script lang="ts" setup>
import { Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'
import ProgressWrapper from './components/progress/ProgressWrapper.vue'
</script>

<template>
  <Toaster :close-button="true" position="top-right" />
  <RouterView />
  <ProgressWrapper />
</template>
