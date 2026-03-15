<script setup lang="ts">
import { useGetFilesFolder } from '@/queries/useFoldersQuery'
import { useRoute } from 'vue-router'

const route = useRoute()

const { data, isLoading } = useGetFilesFolder(route.params.id as string)
</script>

<template>
  <h1>test</h1>

  <p v-if="isLoading">Cargando...</p>

  <p v-else-if="data?.length">
    {{ data[0]?.fecha_creacion }}
  </p>
</template>
