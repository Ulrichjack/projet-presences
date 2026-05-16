<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Mes Séances</h2>
        <p class="text-sm text-gray-500 mt-1">Planning et gestion de vos séances de cours</p>
      </div>
      <button @click="chargerDonnees"
        class="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium px-4 py-2.5 rounded-xl transition-colors">
        <RefreshCw class="w-4 h-4" :class="chargement ? 'animate-spin' : ''" /> Actualiser
      </button>
    </div>

    <!-- Chargement -->
    <div v-if="chargement" class="flex items-center justify-center py-24 text-gray-400">
      <Loader2 class="w-6 h-6 animate-spin mr-2" /> Chargement des séances...
    </div>

    <template v-else>
      <!-- Filtres -->
      <div class="flex flex-wrap gap-3 mb-5">
        <div class="flex gap-1 bg-white border border-gray-200 rounded-xl p-1">
          <button v-for="p in periodes" :key="p.value" @click="filtrePeriode = p.value"
            :class="[
              'px-4 py-1.5 rounded-lg text-sm font-medium transition-all duration-200',
              filtrePeriode === p.value ? 'bg-blue-600 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-50'
            ]">{{ p.label }}</button>
        </div>

        <select v-model="filtreCoursId"
          class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option :value="null">Tous les cours</option>
          <option v-for="c in listeCours" :key="c.id" :value="c.id">{{ c.nom }}</option>
        </select>
      </div>

      <!-- Liste groupée par jour -->
      <div v-if="seancesGroupees.length > 0" class="space-y-6">
        <div v-for="groupe in seancesGroupees" :key="groupe.date">
          <!-- Séparateur avec date -->
          <div class="flex items-center gap-3 mb-3">
            <div class="h-px flex-1 bg-gray-200"></div>
            <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50 px-3 py-1 rounded-full border border-gray-200">
              {{ formatDateGroupe(groupe.date) }}
            </span>
            <div class="h-px flex-1 bg-gray-200"></div>
          </div>

          <div class="space-y-3">
            <div v-for="s in groupe.seances" :key="s.id"
              class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 hover:shadow-md transition-shadow duration-200">
              <div class="flex flex-col sm:flex-row sm:items-center gap-4">
                <!-- Heure -->
                <div class="flex-shrink-0 text-center bg-blue-50 rounded-xl px-4 py-3 w-full sm:w-24">
                  <p class="text-sm font-bold text-blue-700">{{ formatHeure(s.date_heure_debut) }}</p>
                  <p class="text-xs text-blue-500">{{ formatHeure(s.date_heure_fin) }}</p>
                </div>

                <!-- Infos -->
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <h4 class="text-base font-semibold text-gray-900">{{ getNomCours(s.cours_id) }}</h4>
                    <span :class="statutClass(s.statut)"
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium">
                      {{ statutLabel(s.statut) }}
                    </span>
                  </div>
                  <div class="flex flex-wrap items-center gap-3 text-sm text-gray-500">
                    <span v-if="s.salle" class="flex items-center gap-1">
                      <MapPin class="w-3.5 h-3.5" /> {{ s.salle }}
                    </span>
                    <span class="flex items-center gap-1">
                      <Users class="w-3.5 h-3.5" /> {{ s.nbPresents }} présents
                    </span>
                    <span v-if="s.statut !== 'PLANIFIEE'" class="flex items-center gap-1 text-green-600 font-medium">
                      <CheckCircle class="w-3.5 h-3.5" /> {{ s.nbPresents }} pointés
                    </span>
                  </div>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-2 flex-shrink-0">
                  <button v-if="s.statut === 'EN_COURS'"
                    class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium px-4 py-2 rounded-xl transition-colors">
                    <Camera class="w-4 h-4" /> En cours
                  </button>
                  <button v-if="s.statut !== 'EN_COURS' && s.statut !== 'TERMINEE'"
                    class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-xl transition-colors"
                    @click="$emit('aller-scanner')">
                    <Camera class="w-4 h-4" /> Faire l'appel
                  </button>
                  <button @click="voirDetails(s)"
                    class="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium px-4 py-2 rounded-xl transition-colors">
                    <Eye class="w-4 h-4" /> Détails
                  </button>
                                    <!-- NOUVEAU BOUTON : PROJETER QR CODE -->
                  <button v-if="s.statut !== 'TERMINEE'"
                    @click="projeterQRCode(s)"
                    class="inline-flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium px-4 py-2 rounded-xl shadow-sm transition-colors">
                    <QrCode class="w-4 h-4" /> Projeter
                  </button>
                </div>
              </div>

              <!-- Barre de présence -->
              <div v-if="s.nbPresents > 0 && s.statut !== 'PLANIFIEE'" class="mt-4 pt-4 border-t border-gray-100">
                <div class="flex justify-between text-xs text-gray-500 mb-1">
                  <span>{{ s.nbPresents }} pointage{{ s.nbPresents > 1 ? 's' : '' }} enregistré{{ s.nbPresents > 1 ? 's' : '' }}</span>
                  <span class="font-semibold text-green-600">{{ s.nbPresents }} présent{{ s.nbPresents > 1 ? 's' : '' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Aucune séance -->
      <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400">
        <CalendarX class="w-12 h-12 mb-3 opacity-30" />
        <p class="text-sm">Aucune séance pour cette période</p>
      </div>
    </template>

    <!-- ── Modale détail séance ─────────────────────────── -->
    <Teleport to="body">
      <div v-if="modalOuverte"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
        @click.self="modalOuverte = false">
        <div class="bg-white w-full max-w-lg rounded-2xl shadow-2xl">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">Détail de la séance</h3>
            <button @click="modalOuverte = false" class="p-1.5 hover:bg-gray-100 rounded-lg">
              <X class="w-5 h-5 text-gray-500" />
            </button>
          </div>

          <div class="px-6 py-5">
            <!-- Infos séance -->
            <div class="flex items-start gap-3 mb-5 p-4 bg-gray-50 rounded-xl">
              <div>
                <p class="text-base font-semibold text-gray-900">{{ getNomCours(seanceActive?.cours_id) }}</p>
                <p class="text-sm text-gray-500 mt-0.5">
                  {{ formatDateGroupe(seanceActive?.date_heure_debut?.slice(0, 10)) }}
                  · {{ formatHeure(seanceActive?.date_heure_debut) }} – {{ formatHeure(seanceActive?.date_heure_fin) }}
                </p>
                <p v-if="seanceActive?.salle" class="text-xs text-gray-400 mt-1 flex items-center gap-1">
                  <MapPin class="w-3 h-3" /> {{ seanceActive.salle }}
                </p>
              </div>
              <span class="ml-auto text-2xl font-bold text-green-600 flex-shrink-0">
                {{ presencesModal.length }}
              </span>
            </div>

            <!-- Chargement modal -->
            <div v-if="chargementModal" class="flex items-center justify-center py-8 text-gray-400">
              <Loader2 class="w-5 h-5 animate-spin mr-2" /> Chargement des présences...
            </div>

            <!-- Liste présences -->
            <div v-else class="space-y-2 max-h-64 overflow-y-auto">
              <div v-if="presencesModal.length === 0" class="text-center py-8 text-gray-400 text-sm">
                Aucun étudiant pointé pour cette séance
              </div>
              <div v-for="p in presencesModal" :key="p.id"
                class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-700 text-xs font-semibold">
                    {{ p.initiales }}
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ p.prenom }} {{ p.nom }}</p>
                    <p class="text-xs text-gray-400">{{ p.methode }} · {{ p.heure }}</p>
                  </div>
                </div>
                <span :class="p.statut === 'Présent' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
                  class="text-xs font-medium px-2 py-1 rounded-full">
                  {{ p.statut === 'Présent' ? '✓ Présent' : '✗ ' + p.statut }}
                </span>
              </div>
            </div>
          </div>

          <div class="flex justify-end px-6 py-4 border-t border-gray-100 bg-gray-50 rounded-b-2xl">
            <button @click="modalOuverte = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100">
              Fermer
            </button>
          </div>
        </div>
      </div>
    </Teleport>

        <!-- ── Modale Projection QR Code ─────────────────────────── -->
    <Teleport to="body">
      <div v-if="modalQrOuverte" class="fixed inset-0 z-50 flex flex-col items-center justify-center p-8 bg-gray-900 backdrop-blur-md">
        
        <button @click="modalQrOuverte = false" class="absolute top-8 right-8 p-3 bg-white/10 hover:bg-white/20 text-white rounded-full transition-colors">
          <X class="w-8 h-8" />
        </button>

        <div class="text-center mb-10">
          <h2 class="text-5xl font-bold text-white mb-4">{{ getNomCours(seanceActivePourQr?.cours_id) }}</h2>
          <p class="text-2xl text-gray-300">Ouvrez l'application PrésencePro pour flasher ce code</p>
        </div>

        <div class="bg-white p-12 rounded-3xl shadow-2xl">
          <!-- Le fameux QR Code contenant le code de validation de la séance -->
          <qrcode-vue v-if="seanceActivePourQr?.code_validation" :value="seanceActivePourQr.code_validation" :size="400" level="H" />
          <div v-else class="w-[400px] h-[400px] bg-gray-200 animate-pulse rounded-xl"></div>
        </div>

        <div class="mt-10 bg-white/10 px-8 py-4 rounded-2xl border border-white/20 backdrop-blur-sm">
          <p class="text-xl text-white font-mono tracking-[0.5em]">{{ seanceActivePourQr?.code_validation }}</p>
        </div>

      </div>
    </Teleport>

  </div>
</template>

<script setup>
import QrcodeVue from 'qrcode.vue'
import { ref, computed, onMounted } from 'vue'
import { MapPin, Users, Camera, Eye, CheckCircle, X, Loader2, RefreshCw, CalendarX, QrCode } from 'lucide-vue-next' // 👈 AJOUTE QrCode ICI
import api from '@/services/api'

defineEmits(['aller-scanner'])

// ─── État ────────────────────────────────────────────────
const chargement     = ref(true)
const modalOuverte   = ref(false)
const chargementModal = ref(false)
const filtrePeriode  = ref('tout') 
const filtreCoursId  = ref(null)

const listeSeancesRaw = ref([])
const listeCours      = ref([])
const listePresences  = ref([])
const listeEtudiants  = ref([])
const seanceActive    = ref(null)
const presencesModal  = ref([])

const periodes = [
  { value: 'semaine', label: 'Cette semaine' },
  { value: 'mois',   label: 'Ce mois' },
  { value: 'tout',   label: 'Tout' },
]

const modalQrOuverte = ref(false)
const seanceActivePourQr = ref(null)

const projeterQRCode = (seance) => {
  seanceActivePourQr.value = seance
  modalQrOuverte.value = true
}

// ─── Helpers ─────────────────────────────────────────────
const getNomCours = id => listeCours.value.find(c => c.id === id)?.nom ?? 'Cours #' + id

const formatHeure = d => d
  ? new Date(d).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  : '—'

const formatDateGroupe = d => {
  if (!d) return ''
  return new Date(d + (d.length === 10 ? 'T12:00:00' : ''))
    .toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })
}

const getStatut = seance => {
  const now   = new Date()
  const debut = new Date(seance.date_heure_debut)
  const fin   = new Date(seance.date_heure_fin)
  if (now < debut) return 'PLANIFIEE'
  if (now >= debut && now <= fin) return 'EN_COURS'
  return 'TERMINEE'
}

const statutClass = s => {
  if (s === 'EN_COURS')  return 'bg-blue-100 text-blue-700'
  if (s === 'TERMINEE')  return 'bg-green-100 text-green-700'
  if (s === 'ANNULEE')   return 'bg-red-100 text-red-600'
  return 'bg-yellow-100 text-yellow-700'
}

const statutLabel = s => ({
  PLANIFIEE: 'Planifiée', EN_COURS: '● En cours', TERMINEE: 'Terminée', ANNULEE: 'Annulée'
})[s] ?? s

// ─── Séances enrichies ───────────────────────────────────
const listeSeances = computed(() =>
  listeSeancesRaw.value.map(s => {
    const seancePresences = listePresences.value.filter(p => p.seance_id === s.id)
    return {
      ...s,
      statut:    getStatut(s),
      nbPresents: seancePresences.filter(p => p.statut === 'Présent').length,
      dateJour:  s.date_heure_debut?.slice(0, 10) ?? '',
    }
  })
)

// ─── Filtre période ───────────────────────────────────────
const seancesFiltrees = computed(() => {
  const now   = new Date()
  const debut = new Date(now); debut.setHours(0, 0, 0, 0)
  const fin   = new Date(now); fin.setHours(23, 59, 59, 999)

  return listeSeances.value.filter(s => {
    const dateS = new Date(s.date_heure_debut)

    let okPeriode = true
    if (filtrePeriode.value === 'semaine') {
      const lundi = new Date(debut); lundi.setDate(debut.getDate() - debut.getDay() + 1)
      const dimanche = new Date(lundi); dimanche.setDate(lundi.getDate() + 6); dimanche.setHours(23, 59, 59)
      okPeriode = dateS >= lundi && dateS <= dimanche
    } else if (filtrePeriode.value === 'mois') {
      okPeriode = dateS.getFullYear() === now.getFullYear() && dateS.getMonth() === now.getMonth()
    }

    const okCours = !filtreCoursId.value || s.cours_id === filtreCoursId.value
    return okPeriode && okCours
  })
})

// ─── Groupement par jour ──────────────────────────────────
const seancesGroupees = computed(() => {
  const grouped = {}
  seancesFiltrees.value.forEach(s => {
    if (!grouped[s.dateJour]) grouped[s.dateJour] = { date: s.dateJour, seances: [] }
    grouped[s.dateJour].seances.push(s)
  })
  return Object.values(grouped).sort((a, b) => a.date.localeCompare(b.date))
})

// ─── Chargement ──────────────────────────────────────────
const chargerDonnees = async () => {
  chargement.value = true
  try {
    const [resS, resC, resP, resE] = await Promise.all([
      api.get('/seances/mes-seances'),
      api.get('/cours/mes-cours'),
      api.get('/presences/?limit=1000'),
      api.get('/etudiants/?limit=1000'),
    ])
    listeSeancesRaw.value = resS.data
    listeCours.value      = resC.data
    listePresences.value  = resP.data
    listeEtudiants.value  = resE.data
  } catch (e) {
    console.error('Erreur chargement séances :', e)
  } finally {
    chargement.value = false
  }
}

// ─── Modale détail ───────────────────────────────────────
const voirDetails = async (seance) => {
  seanceActive.value = seance
  modalOuverte.value = true
  presencesModal.value = []
  chargementModal.value = true

  try {
    // On filtre les présences déjà chargées
    const pres = listePresences.value.filter(p => p.seance_id === seance.id)
    presencesModal.value = pres.map(p => {
      const e = listeEtudiants.value.find(x => x.id === p.etudiant_id)
      return {
        id:       p.id,
        prenom:   e?.prenom   ?? 'Étudiant',
        nom:      e?.nom      ?? '#' + p.etudiant_id,
        initiales: e ? (e.prenom[0] + e.nom[0]).toUpperCase() : '??',
        methode:  p.methode_pointage,
        heure:    p.heure_pointage
          ? new Date(p.heure_pointage).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
          : '—',
        statut: p.statut,
      }
    })
  } catch (e) {
    console.error('Erreur chargement modal :', e)
  } finally {
    chargementModal.value = false
  }
}

onMounted(chargerDonnees)
</script>