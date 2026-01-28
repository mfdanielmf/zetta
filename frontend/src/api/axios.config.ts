import axios from 'axios'

export default (url = 'http://localhost:8080') => {
  const api = axios.create({
    baseURL: url,
    withCredentials: true
  })

  return api
}
