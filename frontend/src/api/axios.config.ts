import axios from 'axios'

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

  return api
}
