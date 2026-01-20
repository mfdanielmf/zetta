import { createRouter, createWebHistory } from 'vue-router'
import Test from '@/views/TestView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Test
    },
  ],
})

export default router
