<template>
  <div class="max-w-md mx-auto">
    <div class="mb-8 text-center">
      <h2 class="text-2xl font-bold text-gray-900">Scanner le Tableau</h2>
      <p class="text-sm text-gray-500 mt-1">Scannez le QR Code affiché par votre professeur</p>
    </div>

    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 flex flex-col items-center">
      
      <!-- Zone de la caméra -->
      <div class="relative w-full aspect-square bg-gray-900 rounded-2xl overflow-hidden mb-6 shadow-inner flex items-center justify-center">
        <div id="qr-reader-etudiant" class="w-full h-full"></div>

        <div v-if="!scannerActif" class="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
          <Camera class="w-12 h-12 mb-2 opacity-30" />
          <p class="text-sm opacity-50">Caméra éteinte</p>
        </div>

        <!-- Messages de Succès / Erreur -->
        <Transition name="fade">
          <div v-if="messageSucces" class="absolute inset-0 bg-green-500/90 flex flex-col items-center justify-center text-white text-center p-4 z-10">
            <CheckCircle class="w-16 h-16 mb-3" />
            <p class="font-bold text-xl">Présence Validée !</p>
          </div>
        </Transition>
        <Transition name="fade">
          <div v-if="messageErreur" class="absolute inset-0 bg-red-500/90 flex flex-col items-center justify-center text-white text-center p-4 z-10">
            <XCircle class="w-16 h-16 mb-3" />
            <p class="font-bold text-lg">Échec</p>
            <p class="text-sm opacity-90 mt-1">{{ messageErreur }}</p>
          </div>
        </Transition>
      </div>

      <!-- Boutons -->
      <button v-if="!scannerActif" @click="demarrerScanner" class="w-full py-3 rounded-xl text-sm font-bold bg-blue-600 text-white hover:bg-blue-700 transition-all flex justify-center items-center gap-2 shadow-md">
        <Camera class="w-5 h-5" /> Ouvrir la caméra
      </button>
      <button v-else @click="arreterScanner" class="w-full py-3 rounded-xl text-sm font-bold bg-red-50 text-red-600 border border-red-200 hover:bg-red-100 transition-all flex justify-center items-center gap-2">
        <CameraOff class="w-5 h-5" /> Fermer la caméra
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { Camera, CameraOff, CheckCircle, XCircle } from 'lucide-vue-next'
import { Html5Qrcode } from 'html5-qrcode'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const scannerActif = ref(false)
const messageSucces = ref(false)
const messageErreur = ref(null)
let html5QrCode = null

const demarrerScanner = async () => {
  scannerActif.value = true
  html5QrCode = new Html5Qrcode('qr-reader-etudiant')
  
  try {
    await html5QrCode.start(
      { facingMode: "environment" }, 
      { fps: 10, qrbox: { width: 200, height: 200 } }, 
      async (decodedText) => {
        // Dès qu'un QR code est trouvé, on coupe la caméra et on envoie au serveur
        await arreterScanner()
        
        try {
          // On récupère l'ID de l'étudiant dans le token
          const payload = JSON.parse(atob(authStore.token.split('.')[1]))
          const etudiantId = payload.id

          // On appelle la route API de l'étudiant
          await api.post('/scan/etudiant', {
            etudiant_id: etudiantId,
            code_scanne_au_tableau: decodedText // Le code secret lu dans le QR Code
          })

          messageSucces.value = true
          setTimeout(() => { messageSucces.value = false }, 3000)

        } catch (error) {
          messageErreur.value = error.response?.data?.detail || "Erreur de scan"
          setTimeout(() => { messageErreur.value = null }, 4000)
          
          // On relance le scanner après l'erreur pour qu'il puisse réessayer
          setTimeout(() => { demarrerScanner() }, 4500)
        }
      }, 
      () => {}
    )
  } catch (err) {
    scannerActif.value = false
    alert("Impossible d'accéder à la caméra.")
  }
}

const arreterScanner = async () => {
  if (html5QrCode && html5QrCode.isScanning) {
    await html5QrCode.stop()
    html5QrCode.clear()
  }
  scannerActif.value = false
}

onUnmounted(() => {
  arreterScanner()
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>