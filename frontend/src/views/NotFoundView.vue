<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

function volverAtras() {
  router.back()
}
</script>

<template>
  <div class="h-screen flex flex-col gap-5 justify-center items-center">
    <span class="font-bold text-6xl md:text-8xl rebotar">404</span>
    <h1 class="text-gray-500">Parece que esta página no existe.</h1>
    <Button size="lg" class="cursor-pointer" @click="volverAtras">Volver atrás</Button>
  </div>
</template>

<style scoped>
@keyframes rebotar {
  0% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: none;
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
  100% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
}

.rebotar {
  animation: rebotar 1s infinite;
}
</style>
