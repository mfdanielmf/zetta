import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const AuthLayout = () => import("@/layouts/AuthLayout.vue")

const RegisterView = () => import("@/views/auth/RegisterView.vue")
const LoginView = () => import("@/views/auth/LoginView.vue")

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: MainLayout
    },
    {
      path: "/auth",
      redirect: {name: "login"},
      component: AuthLayout,
      children: [
        {
          path: "register",
          name: "register",
          component: RegisterView
        },
        {
          path: "login",
          name:"login",
          component: LoginView
        }
      ]
    }

  ],
})

export default router
