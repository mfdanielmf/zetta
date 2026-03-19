<script setup lang="ts">
import AppSidebar from '@/components/AppSidebar.vue'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
} from '@/components/ui/breadcrumb'
import BreadcrumbSeparator from '@/components/ui/breadcrumb/BreadcrumbSeparator.vue'
import { Separator } from '@/components/ui/separator'
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { useFolderStore } from '@/stores/folder.store'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const carpetasStore = useFolderStore()
const route = useRoute()

const nombreCarpeta = computed(() => {
  // Si no hay carpeta o si el id de la guardada no coinicde con el actual usamos el id, si no el nombre
  if (
    !carpetasStore.hayCarpeta ||
    (carpetasStore.hayCarpeta && carpetasStore.carpetaActiva?.id != route.params.id)
  ) {
    return route.params.id
  }

  return carpetasStore.carpetaActiva?.nombre
})
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <header
        class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12"
      >
        <div class="flex items-center gap-2 px-4">
          <SidebarTrigger class="-ml-1" />
          <Separator orientation="vertical" class="mr-2 data-[orientation=vertical]:h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink as-child>
                  <RouterLink :to="{ name: 'archivos' }">Mis Archivos</RouterLink>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator v-if="nombreCarpeta" />
              <BreadcrumbItem v-if="nombreCarpeta">
                <BreadcrumbLink as-child>
                  {{ nombreCarpeta }}
                </BreadcrumbLink>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
      </header>
      <!-- Contenido aquí -->
      <div class="px-4">
        <RouterView />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
