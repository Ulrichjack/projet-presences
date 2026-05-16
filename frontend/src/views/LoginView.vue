<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4 font-['Inter',sans-serif]">
    
    <!-- Éléments de décoration en arrière-plan -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
    </div>

    <!-- Carte de connexion -->
    <div class="relative w-full max-w-md">
      <div class="backdrop-blur-md bg-white/90 rounded-3xl shadow-2xl p-8 md:p-10 border border-white/20 hover:shadow-2xl transition-shadow duration-300">
        
        <!-- Logo / Titre -->
        <div class="mb-8 text-center">
          
          <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">
            PrésencePro
          </h1>
          <p class="mt-2 text-gray-500 text-sm">Système de gestion de présence</p>
        </div>

        <!-- Titre du formulaire -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">Bienvenue</h2>
          <p class="text-gray-600 text-sm">Connectez-vous à votre compte pour continuer</p>
        </div>

        <!-- Message d'erreur -->
        <transition
          enter-active-class="animate-slideDown"
          leave-active-class="animate-slideUp"
        >
          <div v-if="errorMessage" class="mb-6 flex items-start gap-3 rounded-xl bg-red-50 border border-red-200 p-4 text-sm">
            <svg class="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <p class="text-red-700 font-medium">{{ errorMessage }}</p>
          </div>
        </transition>

        <!-- Message de succès -->
        <transition
          enter-active-class="animate-slideDown"
          leave-active-class="animate-slideUp"
        >
          <div v-if="successMessage" class="mb-6 flex items-start gap-3 rounded-xl bg-green-50 border border-green-200 p-4 text-sm">
            <svg class="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
            <p class="text-green-700 font-medium">{{ successMessage }}</p>
          </div>
        </transition>

        <!-- Formulaire -->
        <form @submit.prevent="handleLogin" class="space-y-5">

          <!-- Champ Email -->
          <div class="group">
            <label for="email" class="block text-sm font-semibold text-gray-700 mb-2.5">Adresse email</label>
            <div class="relative">
              <div class="absolute left-0 top-0 h-full w-12 flex items-center justify-center text-gray-400 group-focus-within:text-blue-600 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <input 
                v-model="email" 
                type="email" 
                id="email" 
                placeholder="admin@ecole.com" 
                required 
                class="w-full h-12 pl-12 pr-4 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 bg-gray-50 focus:bg-white text-gray-900 placeholder-gray-400 transition-all duration-200 outline-none"
              />
            </div>
          </div>

          <!-- Champ Mot de passe -->
          <div class="group">
            <div class="flex items-center justify-between mb-2.5">
              <label for="password" class="block text-sm font-semibold text-gray-700">Mot de passe</label>
              <a href="#" class="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors">Oublié ?</a>
            </div>
            <div class="relative">
              <div class="absolute left-0 top-0 h-full w-12 flex items-center justify-center text-gray-400 group-focus-within:text-blue-600 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <input 
                v-model="password" 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                placeholder="••••••••" 
                required 
                class="w-full h-12 pl-12 pr-12 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 bg-gray-50 focus:bg-white text-gray-900 placeholder-gray-400 transition-all duration-200 outline-none"
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-0 top-0 h-full w-12 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-4.803m5.596-3.856a3.375 3.375 0 11-4.753 4.753m4.753-4.753L3.596 3.596m16.807 16.807L9.172 9.172m0 0a3 3 0 114.243 4.243"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Case à cocher "Se souvenir" -->
          <label class="flex items-center gap-2.5 cursor-pointer group">
            <input 
              v-model="rememberMe" 
              type="checkbox" 
              class="w-4 h-4 accent-blue-600 rounded cursor-pointer"
            />
            <span class="text-sm text-gray-600 group-hover:text-gray-700 transition-colors">Se souvenir de moi</span>
          </label>

          <!-- Bouton de connexion -->
          <button 
            type="submit" 
            :disabled="isLoading"
            class="w-full h-12 mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold rounded-lg transition-all duration-200 flex items-center justify-center gap-2 hover:shadow-lg hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:shadow-none"
          >
            <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isLoading ? 'Connexion…' : 'Connexion sécurisée' }}</span>
          </button>
        </form>

        <!-- Lien d'inscription -->
        <div class="mt-6 text-center border-t border-gray-200 pt-6">
          <p class="text-gray-600 text-sm">
            Vous n'avez pas de compte ?
            <a href="#" class="text-blue-600 font-semibold hover:text-blue-700 transition-colors">S'inscrire maintenant</a>
          </p>
        </div>
      </div>

      <!-- Indicateur de sécurité -->
      <div class="mt-6 flex items-center justify-center gap-2 text-xs text-gray-500">
        <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
        </svg>
        <span>Connexion 100% sécurisée</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api' // <-- 1. On importe notre instance Axios

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const isLoading = ref(false)
const errorMessage = ref(null)
const successMessage = ref(null)

const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  if (!email.value || !password.value) {
    errorMessage.value = 'Veuillez remplir tous les champs'
    return
  }

  isLoading.value = true
  errorMessage.value = null
  successMessage.value = null

  const formData = new URLSearchParams()
  formData.append('username', email.value)
  formData.append('password', password.value)

  try {
    // 2. On utilise Axios ! Plus besoin de mettre http://127... ni les headers compliqués
    const response = await api.post('/login', formData)

    successMessage.value = 'Connexion réussie ! Redirection en cours...'
    
    // Axios met automatiquement la réponse dans 'response.data'
    authStore.sauvegarderToken(response.data.access_token, rememberMe.value)

    // 3. LA CORRECTION DU FORMULAIRE : On vide les champs !
    email.value = ''
    password.value = ''

    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)

  } catch (error) {
    // Gestion des erreurs propre avec Axios
    if (error.response) {
      errorMessage.value = error.response.data.detail || 'Erreur de connexion.'
    } else {
      errorMessage.value = 'Le serveur est inaccessible. Vérifiez votre connexion.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Animations personnalisées */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-12px);
  }
}

.animate-slideDown {
  animation: slideDown 0.3s ease-out;
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}

/* Smooth transitions */
input {
  transition: all 0.2s ease;
}

input:focus {
  transform: translateY(-1px);
}

/* Effet de focus sur le bouton */
button:not(:disabled):active {
  transform: translateY(1px);
}
</style>
