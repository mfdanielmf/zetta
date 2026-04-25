<script setup lang="ts">
import type { SidebarProps } from '@/components/ui/sidebar'

import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
} from 'lucide-vue-next'
import NavMain from '@/components/NavMain.vue'
import NavProjects from '@/components/NavProjects.vue'
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
    {
      name: 'Acme Corp.',
      logo: AudioWaveform,
      plan: 'Startup',
    },
    {
      name: 'Evil Corp.',
      logo: Command,
      plan: 'Free',
    },
  ],

  navMain: [
    {
      title: 'Mi Unidad',
      url: '#',
      icon: SquareTerminal,
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
      icon: Bot,
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
      title: 'Documentation',
      url: '#',
      icon: BookOpen,
      items: [
        {
          title: 'Introduction',
          url: '#',
        },
        {
          title: 'Get Started',
          url: '#',
        },
      ],
    },

    {
      title: 'Settings',
      url: '#',
      icon: Settings2,
      items: [
        {
          title: 'General',
          url: '#',
        },
        {
          title: 'Team',
          url: '#',
        },
      ],
    },
  ],

  projects: [
    {
      name: 'Design Engineering',
      url: '#',
      icon: Frame,
    },
    {
      name: 'Sales & Marketing',
      url: '#',
      icon: PieChart,
    },
    {
      name: 'Travel',
      url: '#',
      icon: Map,
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
      <NavProjects :projects="data.projects" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="authStore.usuario" v-if="authStore.usuario" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
