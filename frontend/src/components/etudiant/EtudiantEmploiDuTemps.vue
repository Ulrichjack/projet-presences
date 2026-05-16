<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-300 overflow-hidden">

    <!-- En-tête -->
    <div class="bg-gray-800 px-6 py-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-bold text-white uppercase tracking-widest">Emplois du Temps</h2>
        <p class="text-xs text-gray-400 mt-1 tracking-wide">Généré depuis la base de données en temps réel</p>
      </div>

      <!-- Navigation semaine -->
      <div class="flex items-center gap-2 bg-white/10 border border-white/20 rounded-xl p-1.5">
        <button @click="changerSemaine(-1)"
          class="px-4 py-2 rounded-lg text-sm font-bold text-white hover:bg-white/20 transition-all">
          ← Préc.
        </button>
        <span class="text-sm font-bold text-white min-w-[220px] text-center tracking-wide">
          {{ textePeriode }}
        </span>
        <button @click="changerSemaine(1)"
          class="px-4 py-2 rounded-lg text-sm font-bold text-white hover:bg-white/20 transition-all">
          Suiv. →
        </button>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="chargement" class="flex items-center justify-center py-24 text-gray-500 gap-3">
      <div class="animate-spin rounded-full h-8 w-8 border-4 border-black border-t-transparent"></div>
      <span class="font-medium text-sm">Chargement de l'emploi du temps...</span>
    </div>

    <!-- Tableau -->
    <div v-else class="overflow-x-auto">
      <table class="w-full border-collapse text-center text-xs" style="min-width: 950px;">

        <!-- En-tête des jours -->
        <thead>
          <tr>
            <th class="border border-gray-300 bg-gray-100 px-3 py-4 font-black text-black text-sm w-28 uppercase tracking-wider">
              Horaire
            </th>
            <th
              v-for="(jour, idx) in joursSemaine"
              :key="jour"
              class="border border-gray-300 px-3 py-4 font-black text-sm uppercase tracking-wider"
              :class="estAujourdhui(idx + 1)
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-black'"
            >
              <div>{{ jour }}</div>
              <div
                class="text-xs font-semibold mt-0.5"
                :class="estAujourdhui(idx + 1) ? 'text-green-100' : 'text-gray-500'"
              >
                {{ datesDuJour[idx] }}
              </div>
              <div v-if="estAujourdhui(idx + 1)"
                class="text-xs font-bold mt-1 bg-white text-green-700 rounded-full px-2 py-0.5 inline-block">
                Aujourd'hui
              </div>
            </th>
          </tr>
        </thead>

        <tbody>
          <template v-for="ligne in lignesGrille" :key="ligne.horaire">

            <!-- LIGNE PAUSE -->
            <tr v-if="ligne.estPause" class="bg-gray-50">
              <td class="border border-gray-300 px-2 py-1.5 text-xs font-bold text-gray-400 italic tracking-wider">
                {{ ligne.horaire }}
              </td>
              <td
                v-for="jour in joursSemaine"
                :key="jour"
                class="border border-gray-300 px-2 py-1.5 text-xs text-gray-400 italic font-semibold tracking-widest"
              >
                —* PAUSE *—
              </td>
            </tr>

            <!-- LIGNE COURS -->
            <tr v-else class="hover:bg-gray-50 transition-colors duration-100">
              <!-- Colonne horaire -->
              <td class="border border-gray-300 px-2 py-3 bg-gray-50">
                <span class="text-xs font-black text-black block">{{ ligne.horaire.split(' - ')[0] }}</span>
                <span class="text-xs text-gray-400 block mt-0.5">{{ ligne.horaire.split(' - ')[1] }}</span>
              </td>

              <!-- Colonnes jours -->
              <td
                v-for="(jour, idx) in joursSemaine"
                :key="jour"
                class="border border-gray-300 p-1 align-middle"
                :class="estAujourdhui(idx + 1) ? 'bg-green-50' : ''"
                style="height: 90px; min-width: 130px;"
              >
                <!-- Cellule avec cours -->
                <div
                  v-if="getSeance(idx + 1, ligne.horaire)"
                  class="flex flex-col items-center justify-center h-full gap-0.5 px-1.5 py-2 rounded border"
                  :class="estAujourdhui(idx + 1)
                    ? 'bg-green-100 border-green-400'
                    : 'bg-gray-900 border-gray-700'"
                  style="min-height: 82px;"
                >
                  <span
                    class="font-black text-xs text-center leading-tight"
                    :class="estAujourdhui(idx + 1) ? 'text-green-900' : 'text-white'"
                  >
                    (CM) {{ getSeance(idx + 1, ligne.horaire).cours }}
                  </span>
                  <span
                    class="text-xs font-bold uppercase tracking-wide text-center leading-tight mt-0.5"
                    :class="estAujourdhui(idx + 1) ? 'text-green-700' : 'text-gray-300'"
                  >
                    {{ getSeance(idx + 1, ligne.horaire).prof }}
                  </span>
                  <span
                    class="text-xs mt-0.5"
                    :class="estAujourdhui(idx + 1) ? 'text-green-600' : 'text-gray-400'"
                  >
                    Salle : {{ getSeance(idx + 1, ligne.horaire).salle }}
                  </span>
                </div>

                <!-- Cellule vide -->
                <div v-else class="h-full flex items-center justify-center">
                  <span class="text-gray-200 text-base">·</span>
                </div>
              </td>
            </tr>
          </template>

          <!-- Aucun cours -->
          <!-- <tr v-if="horairesCoursUniques.length === 0">
            <td colspan="8" class="border border-gray-300 py-16 text-gray-400 italic text-center text-sm">
              🏖️ Aucun cours prévu pour cette semaine.
            </td>
          </tr> -->
        </tbody>
      </table>
    </div>

    <!-- Légende -->
    <div class="px-6 py-3 bg-gray-50 border-t border-gray-200 flex flex-wrap gap-5 text-xs text-gray-600">
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 bg-gray-900 border border-gray-700 rounded"></div>
        <span class="font-medium">Cours planifié</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 bg-green-100 border border-green-400 rounded"></div>
        <span class="font-medium">Cours aujourd'hui</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 bg-gray-50 border border-gray-300 rounded"></div>
        <span class="font-medium text-gray-400 italic">Pause</span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const joursSemaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

const HORAIRES_FIXES = [
  { horaire: '08:00 - 09:50', estPause: false },
  { horaire: '09:50 - 10:10', estPause: true  },
  { horaire: '10:10 - 12:00', estPause: false },
  { horaire: '12:00 - 13:00', estPause: true  },
  { horaire: '13:00 - 14:50', estPause: false },
  { horaire: '14:50 - 15:10', estPause: true  },
  { horaire: '15:10 - 17:00', estPause: false },
]

const toutesLesSeances = ref([])
const decalageSemaine  = ref(0)
const chargement       = ref(true)

const limitesSemaine = computed(() => {
  const date = new Date()
  const jourActuel = date.getDay() || 7
  const lundi = new Date(date)
  lundi.setDate(date.getDate() - jourActuel + 1 + decalageSemaine.value * 7)
  lundi.setHours(0, 0, 0, 0)
  const dimanche = new Date(lundi)
  dimanche.setDate(lundi.getDate() + 6)
  dimanche.setHours(23, 59, 59, 999)
  return { lundi, dimanche }
})

const textePeriode = computed(() => {
  const { lundi, dimanche } = limitesSemaine.value
  const opt = { day: '2-digit', month: '2-digit', year: 'numeric' }
  return `Du ${lundi.toLocaleDateString('fr-FR', opt)} au ${dimanche.toLocaleDateString('fr-FR', opt)}`
})

const datesDuJour = computed(() => {
  const { lundi } = limitesSemaine.value
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(lundi)
    d.setDate(lundi.getDate() + i)
    return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })
  })
})

const estAujourdhui = (jourIndex) => {
  const { lundi, dimanche } = limitesSemaine.value
  const today = new Date()
  if (today < lundi || today > dimanche) return false
  const jourActuel = today.getDay() || 7
  return jourActuel === jourIndex
}

const changerSemaine = (val) => { decalageSemaine.value += val }

const chargerEmploiDuTemps = async () => {
  chargement.value = true
  try {
    const [resSeances, resCours, resEnseignants] = await Promise.all([
      api.get('/seances/mon-emploi-du-temps'), // <-- NOUVELLE ROUTE !
      api.get('/cours/?limit=500'),
      api.get('/enseignants/')
    ])

    const listeCours = resCours.data
    const listeProfs = resEnseignants.data

    toutesLesSeances.value = resSeances.data.map(s => {
      const debut = new Date(s.date_heure_debut)
      const fin   = new Date(s.date_heure_fin)
      let jourIndex = debut.getDay()
      jourIndex = jourIndex === 0 ? 7 : jourIndex
      const fmt = (d) => `${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
      const creneau = trouverCreneauFixe(fmt(debut), fmt(fin))
      const prof = listeProfs.find(p => p.id === s.enseignant_id)
      return {
        dateOriginale: debut,
        jour:   jourIndex,
        heure:  creneau,
        cours:  listeCours.find(c => c.id === s.cours_id)?.nom || 'Inconnu',
        prof:   prof ? `${prof.nom} ${prof.prenom}`.toUpperCase() : 'INCONNU',
        salle:  s.salle || '—'
      }
    })
  } catch (error) {
    console.error('Erreur emploi du temps :', error)
  } finally {
    chargement.value = false
  }
}

const trouverCreneauFixe = (heureDebut, heureFin) => {
  for (const ligne of HORAIRES_FIXES) {
    if (ligne.estPause) continue
    const [debutFix] = ligne.horaire.split(' - ')
    if (heureDebut === debutFix) return ligne.horaire
  }
  return `${heureDebut} - ${heureFin}`
}

const seancesFiltrees = computed(() => {
  const { lundi, dimanche } = limitesSemaine.value
  return toutesLesSeances.value.filter(s => s.dateOriginale >= lundi && s.dateOriginale <= dimanche)
})

const horairesCoursUniques = computed(() => {
  const heures = new Set(seancesFiltrees.value.map(s => s.heure))
  return Array.from(heures)
})

const lignesGrille = computed(() => {
  const horairesFixesCours = HORAIRES_FIXES.map(l => l.horaire)
  const extra = horairesCoursUniques.value
    .filter(h => !horairesFixesCours.includes(h))
    .map(h => ({ horaire: h, estPause: false }))
  return [...HORAIRES_FIXES, ...extra].sort((a, b) =>
    a.horaire.split(' - ')[0].localeCompare(b.horaire.split(' - ')[0])
  )
})

const getSeance = (jourIndex, horaire) =>
  seancesFiltrees.value.find(s => s.jour === jourIndex && s.heure === horaire) || null

onMounted(chargerEmploiDuTemps)
</script>