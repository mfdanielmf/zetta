import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const AuthLayout = () => import("@/layouts/AuthLayout.vue")

const RegisterView = () => import("@/views/auth/RegisterView.vue")

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainLayout
    },
    {
      path: "/auth",
      redirect: {name: "register"}, //Temporal mientras no hago el login. Mejor redirigir a Login
      component: AuthLayout,
      children: [
        {
          path: "register",
          name: "register",
          component: RegisterView
        }
      ]
    }

  ],
})

export default router
