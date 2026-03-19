import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { toast } from 'vue-sonner'
import { useQueryClient } from '@tanstack/vue-query'
import { obtenerArchivosCarpetaService } from '@/services/folder.services'

const MainLayout = () => import('@/layouts/MainLayout.vue')
const AuthLayout = () => import('@/layouts/AuthLayout.vue')

const RegisterView = () => import('@/views/auth/RegisterView.vue')
const LoginView = () => import('@/views/auth/LoginView.vue')
const FilesView = () => import('@/views/StorageView.vue')
const FolderFilesView = () => import('@/views/FolderFilesView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: MainLayout,
      meta: { authRequired: true },
      redirect: { name: 'archivos' },
      children: [
        {
          path: '/storage',
          name: 'archivos',
          component: FilesView,
        },
        {
          path: '/storage/:id',
          name: 'carpeta',
          component: FolderFilesView,
        },
      ],
    },
    {
      path: '/auth',
      redirect: { name: 'login' },
      component: AuthLayout,
      children: [
        {
          path: 'register',
          name: 'register',
          component: RegisterView,
        },
        {
          path: 'login',
          name: 'login',
          component: LoginView,
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  const queryClient = useQueryClient()

  if (to.meta.authRequired) {
    if (authStore.logueado) return

    const logueado = await authStore.obtenerUsuario()

    if (!logueado) {
      toast.info('Inicia sesión para acceder aquí')
      return { name: 'login' }
    }
  }

  if (to.name === 'carpeta') {
    const idCarpeta = to.params.id

    try {
      await queryClient.fetchQuery({
        queryKey: ['archivosCarpeta', authStore.usuario?.id, idCarpeta],
        queryFn: () => obtenerArchivosCarpetaService(idCarpeta as string),
        retry: false,
      })
    } catch {
      return { name: 'archivos', replace: true }
    }
  }
})

export default router
