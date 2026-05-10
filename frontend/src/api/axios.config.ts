import axios from 'axios'

export default (url = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080') => {
  const api = axios.create({
    baseURL: url,
    withCredentials: true,
  })

  return api
}
