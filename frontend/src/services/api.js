import axios from 'axios'
import { useAuthStore } from '../stores/auth'

// On crée une instance d'Axios pré-configurée avec notre URL de base
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// INTERCEPTEUR : Avant CHAQUE requête envoyée au backend...
api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  // ... si on a un Token, on l'accroche automatiquement à la requête !
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

export default api