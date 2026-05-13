import axios from 'axios'
import router from '@/router'

export default (url = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080') => {
  const api = axios.create({
    baseURL: url,
  })

  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('tokenZetta')

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  })

  api.interceptors.response.use(
    (response) => response,
    (error) => {
      const status = error.response?.status
      const detail = error.response?.data?.detail

      if (status === 401 && detail === 'No se proporcionó token') {
        localStorage.removeItem('tokenZetta')

        router.push({ name: 'login' })
      }

      return Promise.reject(error)
    },
  )

  return api
}
