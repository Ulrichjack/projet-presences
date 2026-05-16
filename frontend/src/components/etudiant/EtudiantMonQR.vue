<template>
  <div class="max-w-md mx-auto">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900">Mon QR Code</h2>
      <p class="text-sm text-gray-500 mt-1">Présentez ce code à votre professeur lors de chaque séance</p>
    </div>

    <!-- Carte QR Code -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <!-- Header coloré -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-5 text-white">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
            <span class="text-lg font-bold">{{ initiales }}</span>
          </div>
          <div>
            <p class="font-semibold text-lg">{{ etudiant.prenom }} {{ etudiant.nom }}</p>
            <p class="text-blue-200 text-sm">{{ etudiant.matricule }}</p>
          </div>
        </div>
      </div>

      <!-- QR Code visuel -->
      <div class="p-8 flex flex-col items-center">
        
        <!-- LE VRAI QR CODE EST ICI ! -->
        <div class="w-56 h-56 bg-white border-2 border-gray-200 rounded-2xl p-4 mb-6 shadow-inner flex items-center justify-center">
          <qrcode-vue v-if="etudiant.qr_code" :value="etudiant.qr_code" :size="190" level="H" />
          <div v-else class="animate-pulse w-full h-full bg-gray-200 rounded-xl"></div>
        </div>

        <!-- Matricule -->
        <div class="text-center mb-6">
          <p class="text-xs text-gray-400 uppercase tracking-widest mb-1">Matricule</p>
          <p class="text-lg font-mono font-bold text-gray-900 tracking-wider">{{ etudiant.matricule }}</p>
        </div>

        <!-- Infos filière (En dur pour l'instant car pas dans la DB) -->
        <div class="w-full grid grid-cols-2 gap-3 mb-6">
          <div class="bg-gray-50 rounded-xl p-3 text-center">
            <p class="text-xs text-gray-400 mb-0.5">Filière</p>
            <p class="text-sm font-semibold text-gray-800">Informatique</p>
          </div>
          <div class="bg-gray-50 rounded-xl p-3 text-center">
            <p class="text-xs text-gray-400 mb-0.5">Niveau</p>
            <p class="text-sm font-semibold text-gray-800">L3</p>
          </div>
        </div>

        <!-- Validité -->
        <div class="w-full flex items-center gap-2 bg-green-50 border border-green-200 rounded-xl px-4 py-3">
          <CheckCircle class="w-4 h-4 text-green-600 flex-shrink-0" />
          <div class="flex-1">
            <p class="text-xs font-semibold text-green-700">QR Code valide</p>
            <p class="text-xs text-green-600">Généré par PrésencePro</p>
          </div>
          <span class="text-xs bg-green-600 text-white px-2 py-0.5 rounded-full font-medium">Actif</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { CheckCircle, Download, Share2, Info } from 'lucide-vue-next'
import QrcodeVue from 'qrcode.vue' // <-- IMPORT DE LA LIBRAIRIE
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// L'état de l'étudiant (vide au départ)
const etudiant = ref({
  prenom: 'Chargement...',
  nom: '',
  matricule: '...',
  qr_code: ''
})

const initiales = computed(() => {
  if (!etudiant.value.prenom) return '??'
  return `${etudiant.value.prenom[0] || ''}${etudiant.value.nom[0] || ''}`.toUpperCase()
})

// APPEL API : On récupère les vraies infos de l'étudiant connecté !
const chargerProfil = async () => {
  try {
    // 1. On lit l'ID de l'étudiant caché dans son Token
    const payload = JSON.parse(atob(authStore.token.split('.')[1]))
    const etudiantId = payload.id

    // 2. On demande ses infos au backend
    const response = await api.get(`/etudiants/${etudiantId}`)
    etudiant.value = response.data
  } catch (error) {
    console.error("Erreur de chargement du profil:", error)
  }
}

onMounted(chargerProfil)
</script>