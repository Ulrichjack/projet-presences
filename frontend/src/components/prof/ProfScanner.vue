<template>
  <div>
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900">Scanner – Faire l'appel</h2>
      <p class="text-sm text-gray-500 mt-1">Sélectionnez une séance puis utilisez le QR Code ou la Reconnaissance Faciale</p>
    </div>

    <div v-if="chargement" class="flex items-center justify-center py-24 text-gray-400">
      <Loader2 class="w-6 h-6 animate-spin mr-2" /> Chargement des séances...
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- ── Colonne Scanner ──────────────────────────── -->
      <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
        
        <!-- Tabs QR Code / Visage -->
        <div class="flex border-b border-gray-100">
          <button @click="changerMode('qr')" :class="modeScan === 'qr' ? 'border-b-2 border-blue-600 text-blue-600 bg-blue-50/50' : 'text-gray-500 hover:bg-gray-50'" class="flex-1 py-4 text-sm font-bold flex items-center justify-center gap-2 transition-colors">
            <QrCode class="w-4 h-4" /> QR Code
          </button>
          <button @click="changerMode('visage')" :class="modeScan === 'visage' ? 'border-b-2 border-purple-600 text-purple-600 bg-purple-50/50' : 'text-gray-500 hover:bg-gray-50'" class="flex-1 py-4 text-sm font-bold flex items-center justify-center gap-2 transition-colors">
            <ScanFace class="w-4 h-4" /> Visage (IA)
          </button>
        </div>

        <div class="p-6 flex-1 flex flex-col">
          <!-- Sélection séance -->
          <div class="mb-4">
            <label class="block text-xs font-semibold text-gray-500 uppercase mb-1.5">Séance à pointer</label>
            <select v-model="seanceSelectionneeId" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none">
              <option :value="null" disabled>-- Sélectionner une séance --</option>
              <option v-for="s in seancesDisponibles" :key="s.id" :value="s.id">
                {{ getNomCours(s.cours_id) }} — {{ formatHeure(s.date_heure_debut) }}
              </option>
            </select>
          </div>

          <!-- ================= MODE QR CODE ================= -->
          <div v-show="modeScan === 'qr'" class="flex-1 flex flex-col">
            <div class="relative aspect-video bg-gray-900 rounded-xl overflow-hidden mb-4 flex items-center justify-center shadow-inner">
              <div id="qr-reader" class="w-full h-full"></div>
              <div v-if="!scannerActif && !dernierScan" class="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
                <QrCode class="w-12 h-12 mb-2 opacity-30" />
                <p class="text-sm opacity-50">Caméra inactive</p>
              </div>
              <Transition name="fade">
                <div v-if="dernierScan" class="absolute inset-0 bg-green-500/90 flex flex-col items-center justify-center text-white text-center p-4 z-10">
                  <CheckCircle class="w-14 h-14 mb-3" />
                  <p class="font-bold text-xl">{{ dernierScan.prenom }} {{ dernierScan.nom }}</p>
                  <p class="text-sm opacity-90">Présence validée</p>
                </div>
              </Transition>
              <Transition name="fade">
                <div v-if="erreurScan" class="absolute inset-0 bg-red-500/90 flex flex-col items-center justify-center text-white text-center p-4 z-10">
                  <XCircle class="w-14 h-14 mb-3" />
                  <p class="font-bold text-lg">Échec</p>
                  <p class="text-sm opacity-90 mt-1">{{ erreurScan }}</p>
                </div>
              </Transition>
            </div>
            <div class="flex gap-3 mt-auto">
              <button @click="startScannerQR" :disabled="!seanceSelectionneeId || scannerActif" class="flex-1 py-3 rounded-xl text-sm font-bold bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition-all flex justify-center items-center gap-2">
                <Camera class="w-4 h-4" /> Démarrer
              </button>
              <button @click="stopScannerQR" :disabled="!scannerActif" class="flex-1 py-3 rounded-xl text-sm font-bold bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-50 transition-all flex justify-center items-center gap-2">
                <CameraOff class="w-4 h-4" /> Arrêter
              </button>
            </div>
          </div>

          <!-- ================= MODE VISAGE (IA) ================= -->
          <div v-show="modeScan === 'visage'" class="flex-1 flex flex-col">
            <!-- Liste des étudiants non présents -->
            <div class="mb-4">
              <label class="block text-xs font-semibold text-gray-500 uppercase mb-1.5">Qui est devant la caméra ?</label>
              <select v-model="etudiantAVisage" class="w-full px-3 py-2.5 bg-purple-50 border border-purple-200 text-purple-900 rounded-xl text-sm focus:ring-2 focus:ring-purple-500 outline-none">
                <option :value="null" disabled>-- Choisir l'étudiant --</option>
                <option v-for="e in etudiantsNonPresents" :key="e.id" :value="e.id">
                  {{ e.prenom }} {{ e.nom }} ({{ e.matricule }})
                </option>
              </select>
            </div>

            <!-- Webcam Standard -->
            <div class="relative aspect-video bg-gray-900 rounded-xl overflow-hidden mb-4 flex items-center justify-center shadow-inner">
              <video ref="videoWebcam" class="w-full h-full object-cover" autoplay playsinline></video>
              
              <!-- Messages Superposés -->
              <div v-if="!cameraVisageActive && !dernierScan" class="absolute inset-0 flex flex-col items-center justify-center text-gray-500 bg-gray-900">
                <ScanFace class="w-12 h-12 mb-2 opacity-30" />
                <p class="text-sm opacity-50">Webcam désactivée</p>
              </div>
              <div v-if="verificationEnCours" class="absolute inset-0 bg-black/60 flex flex-col items-center justify-center text-white backdrop-blur-sm z-10">
                <Loader2 class="w-10 h-10 animate-spin text-purple-400 mb-3" />
                <p class="font-bold text-sm animate-pulse">L'IA analyse le visage...</p>
              </div>
              <Transition name="fade">
                <div v-if="dernierScan && modeScan === 'visage'" class="absolute inset-0 bg-green-500/90 flex flex-col items-center justify-center text-white text-center p-4 z-20">
                  <CheckCircle class="w-14 h-14 mb-3" />
                  <p class="font-bold text-xl">{{ dernierScan.prenom }}</p>
                  <p class="text-sm opacity-90">Identité confirmée !</p>
                </div>
              </Transition>
              <Transition name="fade">
                <div v-if="erreurScan && modeScan === 'visage'" class="absolute inset-0 bg-red-500/90 flex flex-col items-center justify-center text-white text-center p-4 z-20">
                  <AlertTriangle class="w-14 h-14 mb-3" />
                  <p class="font-bold text-lg">Alerte Imposteur</p>
                  <p class="text-sm opacity-90 mt-1">{{ erreurScan }}</p>
                </div>
              </Transition>
            </div>

            <!-- Canvas caché pour capturer la photo -->
            <canvas ref="canvasWebcam" class="hidden"></canvas>

            <div class="flex gap-3 mt-auto">
              <!-- Bouton Allumer/Eteindre -->
              <button v-if="!cameraVisageActive" @click="startCameraVisage" :disabled="!seanceSelectionneeId" class="flex-1 py-3 rounded-xl text-sm font-bold bg-gray-800 text-white hover:bg-gray-900 disabled:opacity-50 transition-all">
                Allumer Webcam
              </button>
              <button v-else @click="stopCameraVisage" class="flex-1 py-3 rounded-xl text-sm font-bold bg-gray-100 text-gray-700 hover:bg-gray-200 transition-all">
                Éteindre
              </button>

              <!-- Bouton Capturer -->
              <button @click="capturerEtVerifier" :disabled="!cameraVisageActive || !etudiantAVisage || verificationEnCours" class="flex-[2] py-3 rounded-xl text-sm font-bold bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 transition-all flex justify-center items-center gap-2 shadow-md">
                <ScanFace class="w-4 h-4" /> Vérifier l'identité
              </button>
            </div>
          </div>

        </div>
      </div>

      <!-- ── Colonne Présences ───────────────────────── -->
      <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 class="text-base font-semibold text-gray-900">Présences enregistrées</h3>
          <div class="text-right">
            <p class="text-2xl font-bold text-green-600">{{ presents.length }}</p>
            <p class="text-xs text-gray-500">présents</p>
          </div>
        </div>

        <div v-if="chargementPresences" class="flex items-center justify-center py-10 text-gray-400">
          <Loader2 class="w-5 h-5 animate-spin mr-2" /> Chargement...
        </div>

        <div v-else class="overflow-y-auto flex-1 max-h-96">
          <div v-if="presents.length === 0" class="flex flex-col items-center justify-center py-12 text-gray-400">
            <Users class="w-10 h-10 mb-2 opacity-30" />
            <p class="text-sm">Aucune présence enregistrée</p>
          </div>

          <div v-for="(p, i) in presents" :key="p.id ?? i" class="flex items-center gap-3 px-6 py-3 border-b border-gray-50 hover:bg-gray-50">
            <span class="text-xs font-mono text-gray-400 w-6">{{ i + 1 }}</span>
            <div class="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-700 text-xs font-bold">
              {{ p.initiales }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ p.prenom }} {{ p.nom }}</p>
              <p class="text-xs text-gray-400 font-medium" :class="p.methode.includes('Visage') ? 'text-purple-500' : 'text-blue-500'">
                {{ p.methode }}
              </p>
            </div>
            <p class="text-xs text-gray-400">{{ p.heure }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Camera, CameraOff, CheckCircle, XCircle, QrCode, Users, ScanFace, Loader2, AlertTriangle } from 'lucide-vue-next'
import { Html5Qrcode } from 'html5-qrcode'
import api from '@/services/api'

// --- ÉTAT GLOBAL ---
const chargement = ref(true)
const chargementPresences = ref(false)
const seanceSelectionneeId = ref(null) // <-- CORRECTION : On stocke juste l'ID
const seancesDisponibles = ref([])
const listeCours = ref([])
const listeEtudiants = ref([])
const presents = ref([])
const dernierScan = ref(null)
const erreurScan = ref(null)
let timerScan = null

// --- ÉTAT QR CODE ---
const modeScan = ref('qr') // 'qr' ou 'visage'
const scannerActif = ref(false)
let html5QrCode = null

// --- ÉTAT VISAGE (IA) ---
const etudiantAVisage = ref(null)
const videoWebcam = ref(null)
const canvasWebcam = ref(null)
const cameraVisageActive = ref(false)
const verificationEnCours = ref(false)
let streamMedia = null

// --- COMPUTED ---
const etudiantsNonPresents = computed(() => {
  const idsPresents = presents.value.map(p => p.etudiant_id)
  return listeEtudiants.value.filter(e => !idsPresents.includes(e.id))
})

// --- HELPERS ---
const getNomCours = id => listeCours.value.find(c => c.id === id)?.nom ?? 'Cours #' + id
const formatHeure = d => d ? new Date(d).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '—'
const enrichirEtudiant = (etudiantId, methode, heurePointage) => {
  const e = listeEtudiants.value.find(x => x.id === etudiantId)
  return {
    etudiant_id: etudiantId,
    prenom: e?.prenom ?? 'Étudiant',
    nom: e?.nom ?? '#' + etudiantId,
    initiales: e ? (e.prenom[0] + e.nom[0]).toUpperCase() : '??',
    methode,
    heure: heurePointage ? new Date(heurePointage).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : formatHeure(new Date()),
  }
}

// --- INITIALISATION ---
const chargerDonnees = async () => {
  try {
    const [resS, resC, resE] = await Promise.all([
      api.get('/seances/mes-seances'),
      api.get('/cours/mes-cours'),
      api.get('/etudiants/?limit=1000'),
    ])
    seancesDisponibles.value = resS.data
    listeCours.value = resC.data
    listeEtudiants.value = resE.data
  } catch (e) { console.error('Erreur chargement :', e) } 
  finally { chargement.value = false }
}

// <-- CORRECTION : On écoute les changements de l'ID
watch(seanceSelectionneeId, async (newId) => {
  stopScannerQR()
  stopCameraVisage()
  presents.value = []
  
  if (!newId) return
  
  chargementPresences.value = true
  try {
    const res = await api.get('/presences/?limit=1000')
    const presencesDeCetteSeance = res.data.filter(p => p.seance_id === newId)
    
    presents.value = presencesDeCetteSeance.map(p => ({
      id: p.id, 
      ...enrichirEtudiant(p.etudiant_id, p.methode_pointage, p.heure_pointage)
    }))
  } catch (e) { 
    console.error('Erreur chargement présences:', e) 
  } finally { 
    chargementPresences.value = false 
  }
})

const changerMode = (mode) => {
  modeScan.value = mode
  if (mode === 'qr') { stopCameraVisage() } 
  else { stopScannerQR() }
}

// ================= LOGIQUE QR CODE =================
const startScannerQR = async () => {
  scannerActif.value = true
  html5QrCode = new Html5Qrcode('qr-reader')
  try {
    await html5QrCode.start({ facingMode: "environment" }, { fps: 10, qrbox: { width: 250, height: 250 } }, async (decodedText) => {
      await html5QrCode.stop()
      try {
        const res = await api.post('/scan/prof', { qr_code_texte: decodedText })
        gererSuccesScan(res.data)
      } catch (err) { gererErreurScan(err) }
    }, () => {})
  } catch (err) { scannerActif.value = false; alert("Erreur Caméra") }
}

const stopScannerQR = async () => {
  if (html5QrCode && html5QrCode.isScanning) { await html5QrCode.stop(); html5QrCode.clear() }
  scannerActif.value = false
}

// ================= LOGIQUE VISAGE (IA) =================
const startCameraVisage = async () => {
  try {
    streamMedia = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
    if (videoWebcam.value) videoWebcam.value.srcObject = streamMedia
    cameraVisageActive.value = true
  } catch (err) { alert("Impossible d'accéder à la webcam. Vérifiez les permissions.") }
}

const stopCameraVisage = () => {
  if (streamMedia) { streamMedia.getTracks().forEach(t => t.stop()); streamMedia = null }
  if (videoWebcam.value) videoWebcam.value.srcObject = null
  cameraVisageActive.value = false
}

const capturerEtVerifier = () => {
  verificationEnCours.value = true
  const canvas = canvasWebcam.value
  const video = videoWebcam.value
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)

  canvas.toBlob(async (blob) => {
    const fd = new FormData()
    fd.append('seance_id', seanceSelectionneeId.value) // <-- CORRECTION ICI
    fd.append('etudiant_id', etudiantAVisage.value)
    fd.append('photo_webcam', blob, 'capture.jpg')

    try {
      const res = await api.post('/scan/visage', fd)
      etudiantAVisage.value = null 
      gererSuccesScan(res.data)
    } catch (err) {
      gererErreurScan(err)
    } finally {
      verificationEnCours.value = false
    }
  }, 'image/jpeg', 0.9)
}

// --- GESTION COMMUNE DES RÉSULTATS ---
const gererSuccesScan = (data) => {
  const info = enrichirEtudiant(data.etudiant_id, data.methode_pointage, data.heure_pointage)
  dernierScan.value = info
  presents.value.unshift({ id: data.id, ...info })
  clearTimeout(timerScan)
  timerScan = setTimeout(() => { dernierScan.value = null; if(modeScan.value === 'qr') startScannerQR() }, 2500)
}

const gererErreurScan = (err) => {
  erreurScan.value = err.response?.data?.detail ?? 'Erreur inconnue'
  clearTimeout(timerScan)
  timerScan = setTimeout(() => { erreurScan.value = null; if(modeScan.value === 'qr') startScannerQR() }, 3000)
}

onMounted(chargerDonnees)
onUnmounted(() => { stopScannerQR(); stopCameraVisage(); clearTimeout(timerScan) })
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>