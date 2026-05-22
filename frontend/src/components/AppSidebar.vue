<script setup lang="ts">
import type { SidebarProps } from '@/components/ui/sidebar'

import { GalleryVerticalEnd, HardDrive, Share2, Star } from 'lucide-vue-next'
import NavMain from '@/components/NavMain.vue'
import NavUser from '@/components/NavUser.vue'
import TeamSwitcher from '@/components/TeamSwitcher.vue'

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@/components/ui/sidebar'
import { useAuthStore } from '@/stores/auth.store'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: 'icon',
})

const authStore = useAuthStore()
const route = useRoute()

const isActive = (path: string) => route.path.startsWith(path)

const data = computed(() => ({
  teams: [
    {
      name: 'Zetta',
      logo: GalleryVerticalEnd,
      plan: 'Enterprise',
    },
  ],

  navMain: [
    {
      title: 'Mi Unidad',
      url: '#',
      icon: HardDrive,
      isActive: route.path.startsWith('/storage') || isActive('/trash'),
      items: [
        {
          title: 'Almacenamiento',
          url: '/storage',
          isActive: isActive('/storage'),
        },
        {
          title: 'Papelera',
          url: '/trash',
          isActive: isActive('/trash'),
        },
      ],
    },
    {
      title: 'Compartido',
      url: '#',
      icon: Share2,
      isActive: route.path.startsWith('/shared'),
      items: [
        {
          title: 'Compartido conmigo',
          url: '/shared/received',
          isActive: isActive('/shared/received'),
        },
        {
          title: 'Compartido por mí',
          url: '/shared/sent',
          isActive: isActive('/shared/sent'),
        },
      ],
    },
    {
      title: 'Favoritos',
      url: '#',
      icon: Star,
      isActive: route.path.startsWith('/favorite'),
      items: [
        {
          title: 'Mis favoritos',
          url: '/favorite',
          isActive: isActive('/favorite'),
        },
      ],
    },
  ],
}))
</script>

<template>
  <Sidebar v-bind="props">
    <SidebarHeader>
      <TeamSwitcher :teams="data.teams" />
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="authStore.usuario" v-if="authStore.usuario" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
