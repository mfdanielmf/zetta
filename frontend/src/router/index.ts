import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { toast } from 'vue-sonner'

const MainLayout = () => import("@/layouts/MainLayout.vue")
const AuthLayout = () => import("@/layouts/AuthLayout.vue")

const RegisterView = () => import("@/views/auth/RegisterView.vue")
const LoginView = () => import("@/views/auth/LoginView.vue")

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: MainLayout,
      meta: { authRequired: true }
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

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (to.meta.authRequired){
    if (authStore.logueado) return

    const logueado = await authStore.obtenerUsuario()

    if (!logueado){
      toast.info("Inicia sesión para acceder aquí")
      return { name: "login" }
    }
  }

})

export default router
