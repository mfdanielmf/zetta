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

const route = useRoute()
const carpetasStore = useFolderStore()

const mainBreadcrumb = computed(() => {
  if (route.name === 'papelera' || route.path.startsWith('/trash')) {
    return {
      name: 'papelera',
      titulo: 'Papelera',
    }
  } else {
    return {
      name: 'archivos',
      titulo: 'Mis Archivos',
    }
  }
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
                  <RouterLink :to="{ name: mainBreadcrumb.name }">
                    {{ mainBreadcrumb.titulo }}
                  </RouterLink>
                </BreadcrumbLink>
              </BreadcrumbItem>

              <template v-for="(carpeta, index) in carpetasStore.carpetaActiva" :key="carpeta.id">
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  <BreadcrumbLink as-child>
                    <RouterLink
                      :to="{ name: 'carpeta', params: { id: carpeta.id } }"
                      :class="{
                        'font-bold text-black pointer-events-none':
                          index === carpetasStore.carpetaActiva.length - 1,
                      }"
                      @click="carpetasStore.setCarpetaActiva(carpeta.id, carpeta.nombre)"
                    >
                      {{ carpeta.nombre }}
                    </RouterLink>
                  </BreadcrumbLink>
                </BreadcrumbItem>
              </template>
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
