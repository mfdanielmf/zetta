import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { toast } from 'vue-sonner'
import { useQueryClient } from '@tanstack/vue-query'
import { obtenerArchivosCarpetaService } from '@/services/folder.services'
import { useFolderStore } from '@/stores/folder.store'
import { useUploadStore } from '@/stores/upload.store'
import { useDownloadStore } from '@/stores/download.store'
import { useSelectedStore } from '@/stores/selected.store'

const MainLayout = () => import('@/layouts/MainLayout.vue')
const AuthLayout = () => import('@/layouts/AuthLayout.vue')

const RegisterView = () => import('@/views/auth/RegisterView.vue')
const LoginView = () => import('@/views/auth/LoginView.vue')
const FilesView = () => import('@/views/storage/StorageView.vue')
const FolderFilesView = () => import('@/views/storage/FolderFilesView.vue')
const PapeleraView = () => import('@/views/trash/PapeleraView.vue')
const FolderFilesPapeleraView = () => import('@/views/trash/FolderFilesPapeleraView.vue')
const ReceivedView = () => import('@/views/shared/ReceivedView.vue')
const SentView = () => import('@/views/shared/SentView.vue')
const SharedFolderView = () => import('@/views/shared/SharedFolderView.vue')
const ReceivedFolderView = () => import('@/views/shared/ReceivedFolderView.vue')
const NotFoundView = () => import('@/views/NotFoundView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      meta: { authRequired: true },
      redirect: { name: 'archivos' },
      children: [
        {
          path: 'storage',
          children: [
            {
              path: '',
              name: 'archivos',
              component: FilesView,
            },
            {
              path: ':id',
              name: 'carpeta',
              component: FolderFilesView,
            },
          ],
        },
        {
          path: 'trash',
          children: [
            {
              path: '',
              name: 'papelera',
              component: PapeleraView,
            },
            {
              path: ':id',
              name: 'carpetaPapelera',
              component: FolderFilesPapeleraView,
            },
          ],
        },
        {
          path: 'shared',
          redirect: { name: 'recibidos' },
          children: [
            {
              path: 'received',
              children: [
                {
                  path: '',
                  name: 'recibidos',
                  component: ReceivedView,
                },
                {
                  path: ':id',
                  name: 'carpetaRecibida',
                  component: ReceivedFolderView,
                },
              ],
            },
            {
              path: 'sent',
              children: [
                {
                  path: '',
                  name: 'compartidos',
                  component: SentView,
                },
                {
                  path: ':id',
                  name: 'carpetaCompartida',
                  component: SharedFolderView,
                },
              ],
            },
          ],
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
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: NotFoundView,
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  const uploadStore = useUploadStore()
  const downloadStore = useDownloadStore()
  const queryClient = useQueryClient()
  const selectedStore = useSelectedStore()

  selectedStore.reset()

  if (to.meta.authRequired) {
    if (authStore.logueado) return

    const logueado = await authStore.obtenerUsuario()

    if (!logueado) {
      toast.info('Inicia sesión para acceder aquí')

      uploadStore.reset()
      downloadStore.reset()

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

  if (to.name === 'login' || to.name === 'register') {
    uploadStore.reset()
    downloadStore.reset()
  }
})

// Resetear breadcrumb al salir de los detalles de la carpeta
router.afterEach((to) => {
  const folderStore = useFolderStore()

  if (
    to.name != 'carpeta' &&
    to.name != 'carpetaPapelera' &&
    to.name != 'carpetaCompartida' &&
    to.name != 'carpetaRecibida'
  ) {
    folderStore.limpiarCarpetas()
  }
})

export default router
