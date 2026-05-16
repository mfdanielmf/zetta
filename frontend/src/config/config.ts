export default {
  LIMITE_FETCH: 25,
  MAX_UPLOAD_SIZE: Number(import.meta.env.VITE_MAX_UPLOAD_SIZE) || 10 * 1024 * 1024,
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080',
}
