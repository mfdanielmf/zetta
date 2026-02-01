<script lang="ts" setup>
import { Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'
</script>

<template>
  <Toaster :close-button="true" position="top-right" />
  <RouterView />
</template>
