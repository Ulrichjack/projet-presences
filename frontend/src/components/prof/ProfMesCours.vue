<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Mes Cours</h2>
        <p class="text-sm text-gray-500 mt-1">
          <template v-if="!chargement">{{ coursList.length }} cours assignés</template>
          <template v-else>Chargement...</template>
        </p>
      </div>
      <button @click="chargerDonnees"
        class="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium px-4 py-2.5 rounded-xl transition-colors">
        <RefreshCw class="w-4 h-4" :class="chargement ? 'animate-spin' : ''" /> Actualiser
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="chargement" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div v-for="i in 3" :key="i" class="bg-white rounded-2xl border border-gray-200 h-64 animate-pulse">
        <div class="h-2 bg-gray-200 rounded-t-2xl"></div>
        <div class="p-6 space-y-3">
          <div class="h-4 bg-gray-100 rounded w-1/3"></div>
          <div class="h-5 bg-gray-100 rounded w-2/3"></div>
          <div class="h-4 bg-gray-100 rounded w-full"></div>
        </div>
      </div>
    </div>

    <template v-else>
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        <div v-for="(c, idx) in coursList" :key="c.id"
          class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200">
          <div class="h-2" :class="COULEURS[idx % COULEURS.length]"></div>
          <div class="p-6">
            <div class="flex items-start justify-between mb-3">
              <span class="text-xs font-mono font-semibold bg-gray-100 text-gray-600 px-2 py-1 rounded-lg">{{ c.code }}</span>
              <span class="text-xs font-medium bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full">{{ c.niveau }}</span>
            </div>
            <h3 class="text-base font-semibold text-gray-900 mb-1">{{ c.nom }}</h3>
            <p class="text-sm text-gray-500 mb-5 line-clamp-2">{{ c.description || 'Aucune description.' }}</p>

            <div class="grid grid-cols-3 gap-3 mb-5">
              <div class="text-center p-2 bg-gray-50 rounded-xl">
                <p class="text-lg font-bold text-gray-900">{{ c.stats.nbEtudiants }}</p>
                <p class="text-xs text-gray-500">Étudiants</p>
              </div>
              <div class="text-center p-2 bg-gray-50 rounded-xl">
                <p class="text-lg font-bold text-gray-900">{{ c.stats.totalSeances }}</p>
                <p class="text-xs text-gray-500">Séances</p>
              </div>
              <div class="text-center p-2 rounded-xl"
                :class="c.stats.tauxPresence >= 75 ? 'bg-green-50' : c.stats.tauxPresence > 0 ? 'bg-red-50' : 'bg-gray-50'">
                <p class="text-lg font-bold"
                  :class="c.stats.tauxPresence >= 75 ? 'text-green-700' : c.stats.tauxPresence > 0 ? 'text-red-600' : 'text-gray-400'">
                  {{ c.stats.tauxPresence }}%
                </p>
                <p class="text-xs"
                  :class="c.stats.tauxPresence >= 75 ? 'text-green-600' : c.stats.tauxPresence > 0 ? 'text-red-500' : 'text-gray-400'">
                  Présence
                </p>
              </div>
            </div>

            <div class="mb-5">
              <div class="flex justify-between text-xs text-gray-500 mb-1">
                <span>Taux de présence</span><span>{{ c.stats.tauxPresence }}%</span>
              </div>
              <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-2 rounded-full transition-all duration-700"
                  :class="c.stats.tauxPresence >= 75 ? 'bg-green-500' : 'bg-red-400'"
                  :style="{ width: c.stats.tauxPresence + '%' }"></div>
              </div>
            </div>

            <div class="flex items-center gap-2 text-sm text-gray-600 border-t border-gray-100 pt-4">
              <Calendar class="w-4 h-4 text-gray-400 flex-shrink-0" />
              <span v-if="c.stats.seanceEnCours" class="flex items-center gap-1.5 text-green-600 font-medium text-sm">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse inline-block"></span>
                En cours maintenant
              </span>
              <span v-else-if="c.stats.prochainSeance">
                Prochaine : <strong class="ml-1">{{ c.stats.prochainSeance }}</strong>
              </span>
              <span v-else class="text-gray-400 italic text-xs">Aucune séance à venir</span>
            </div>
          </div>
        </div>

        <div v-if="coursList.length === 0" class="col-span-3 flex flex-col items-center justify-center py-20 text-gray-400">
          <BookOpen class="w-12 h-12 mb-3 opacity-30" />
          <p class="text-sm">Aucun cours assigné pour le moment</p>
        </div>
      </div>

      <!-- Étudiants à risque -->
      <div v-if="etudiantsARisque.length > 0" class="mt-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <AlertTriangle class="w-5 h-5 text-red-500" />
          Étudiants à risque (présence &lt; 70%)
        </h3>
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Étudiant</th>
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Cours</th>
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Présences</th>
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Taux</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="e in etudiantsARisque" :key="e.cle" class="hover:bg-gray-50">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center text-red-600 text-xs font-semibold">
                        {{ e.initiales }}
                      </div>
                      <p class="text-sm font-medium text-gray-900">{{ e.prenom }} {{ e.nom }}</p>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-600">{{ e.cours }}</td>
                  <td class="px-6 py-4 text-sm font-semibold text-red-600">{{ e.presents }} / {{ e.total }}</td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                      <div class="h-1.5 w-16 bg-gray-100 rounded-full overflow-hidden">
                        <div class="h-1.5 bg-red-400 rounded-full" :style="{ width: e.taux + '%' }"></div>
                      </div>
                      <span class="text-sm text-red-600 font-medium">{{ e.taux }}%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Calendar, AlertTriangle, RefreshCw, BookOpen } from 'lucide-vue-next'
import api from '@/services/api'

const COULEURS = ['bg-blue-500', 'bg-purple-500', 'bg-teal-500', 'bg-orange-500', 'bg-pink-500', 'bg-indigo-500']

const chargement    = ref(true)
const listCoursRaw  = ref([])
const listSeances   = ref([])
const listPresences = ref([])
const listEtudiants = ref([])

const formatHeure = d => d
  ? new Date(d).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  : '—'

const coursList = computed(() =>
  listCoursRaw.value.map(c => {
    const now          = new Date()
    // Toutes les séances de ce cours (peu importe la date)
    const seancesCours = listSeances.value.filter(s => s.cours_id === c.id)
    const totalSeances = seancesCours.length

    // Séance en cours right now
    const seanceEnCours = seancesCours.some(
      s => new Date(s.date_heure_debut) <= now && now <= new Date(s.date_heure_fin)
    )

    // Prochaine séance future
    const prochaine = seancesCours
      .filter(s => new Date(s.date_heure_debut) > now)
      .sort((a, b) => new Date(a.date_heure_debut) - new Date(b.date_heure_debut))[0]

    const prochainSeance = prochaine
      ? new Date(prochaine.date_heure_debut).toLocaleDateString('fr-FR', {
          weekday: 'short', day: 'numeric', month: 'short'
        }) + ' ' + formatHeure(prochaine.date_heure_debut)
      : null

    // Présences pour toutes les séances de ce cours
    const seanceIds      = seancesCours.map(s => s.id)
    const presencesCours = listPresences.value.filter(p => seanceIds.includes(p.seance_id))
    const presentes      = presencesCours.filter(p => p.statut === 'Présent')
    const nbEtudiants    = new Set(presencesCours.map(p => p.etudiant_id)).size
    const tauxPresence   = presencesCours.length > 0
      ? Math.round((presentes.length / presencesCours.length) * 100)
      : 0

    return { ...c, stats: { nbEtudiants, totalSeances, tauxPresence, prochainSeance, seanceEnCours } }
  })
)

const etudiantsARisque = computed(() => {
  const risque = []
  listCoursRaw.value.forEach(c => {
    const seanceIds = listSeances.value.filter(s => s.cours_id === c.id).map(s => s.id)
    if (!seanceIds.length) return
    const parEtudiant = {}
    listPresences.value.filter(p => seanceIds.includes(p.seance_id)).forEach(p => {
      if (!parEtudiant[p.etudiant_id]) parEtudiant[p.etudiant_id] = { total: 0, presents: 0 }
      parEtudiant[p.etudiant_id].total++
      if (p.statut === 'Présent') parEtudiant[p.etudiant_id].presents++
    })
    Object.entries(parEtudiant).forEach(([id, s]) => {
      const taux = Math.round((s.presents / s.total) * 100)
      if (taux < 70) {
        const e = listEtudiants.value.find(x => x.id === parseInt(id))
        risque.push({
          cle: `${id}-${c.id}`,
          prenom: e?.prenom ?? 'Étudiant', nom: e?.nom ?? '#' + id,
          initiales: e ? (e.prenom[0] + e.nom[0]).toUpperCase() : '??',
          cours: c.nom, presents: s.presents, total: s.total, taux,
        })
      }
    })
  })
  return risque.sort((a, b) => a.taux - b.taux)
})

const chargerDonnees = async () => {
  chargement.value = true
  try {
    const [resC, resS, resP, resE] = await Promise.all([
      api.get('/cours/mes-cours'),
      api.get('/seances/mes-seances'),
      api.get('/presences/?limit=1000'),
      api.get('/etudiants/?limit=1000'),
    ])
    listCoursRaw.value  = resC.data
    listSeances.value   = resS.data
    listPresences.value = resP.data
    listEtudiants.value = resE.data
  } catch (e) {
    console.error('Erreur mes cours :', e)
  } finally {
    chargement.value = false
  }
}

onMounted(chargerDonnees)
</script>