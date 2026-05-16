import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  // 1. L'état (les variables globales)
  const token = ref(localStorage.getItem('authToken') || sessionStorage.getItem('authToken') || null)

  // 2. Les "getters" (des questions qu'on peut poser au magasin)
  const estConnecte = computed(() => token.value !== null)

  // 3. Les actions (les fonctions pour modifier l'état)
  function sauvegarderToken(nouveauToken, seSouvenir = false) {
    token.value = nouveauToken
    if (seSouvenir) {
      localStorage.setItem('authToken', nouveauToken)
    } else {
      sessionStorage.setItem('authToken', nouveauToken)
    }
  }

  function deconnexion() {
    token.value = null
    localStorage.removeItem('authToken')
    sessionStorage.removeItem('authToken')
  }

  return { token, estConnecte, sauvegarderToken, deconnexion }
})