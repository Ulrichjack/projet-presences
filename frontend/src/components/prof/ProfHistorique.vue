<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Historique des Appels</h2>
        <p class="text-sm text-gray-500 mt-1">Consultez et exportez les enregistrements de présence</p>
      </div>
      <button @click="exporterCSV"
        class="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium px-4 py-2.5 rounded-xl transition-colors">
        <Download class="w-4 h-4" /> Exporter CSV
      </button>
    </div>

    <!-- Chargement -->
    <div v-if="chargement" class="flex items-center justify-center py-24 text-gray-400">
      <Loader2 class="w-6 h-6 animate-spin mr-2" /> Chargement des données...
    </div>

    <!-- Erreur -->
    <div v-else-if="erreur" class="flex flex-col items-center justify-center py-24 text-red-400">
      <AlertCircle class="w-8 h-8 mb-2" />
      <p class="text-sm">{{ erreur }}</p>
      <button @click="chargerDonnees" class="mt-3 text-sm text-blue-600 hover:underline">Réessayer</button>
    </div>

    <template v-else>
      <!-- Filtres -->
      <div class="flex flex-wrap gap-3 mb-5">
        <div class="relative flex-1 min-w-48">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input v-model="recherche" type="text" placeholder="Rechercher un étudiant..."
            class="w-full pl-9 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <select v-model="filtreCours"
          class="bg-white border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option :value="null">Tous les cours</option>
          <option v-for="c in listeCours" :key="c.id" :value="c.id">{{ c.nom }}</option>
        </select>

        <select v-model="filtreStatut"
          class="bg-white border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">Tout</option>
          <option value="Présent">Présents</option>
          <option value="Absent">Absents</option>
        </select>
      </div>

      <!-- Tableau -->
      <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-100 bg-gray-50">
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Étudiant</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Cours</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Heure scan</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Méthode</th>
                <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Statut</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="r in historiquePagine" :key="r.id"
                class="hover:bg-gray-50 transition-colors duration-150">
                <!-- Étudiant -->
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold flex-shrink-0"
                      :class="r.statut === 'Présent' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'">
                      {{ r.etudiant ? (r.etudiant.prenom[0] + r.etudiant.nom[0]).toUpperCase() : '??' }}
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">
                        {{ r.etudiant?.prenom ?? '—' }} {{ r.etudiant?.nom ?? '' }}
                      </p>
                      <p class="text-xs text-gray-400">{{ r.etudiant?.matricule ?? 'ID: ' + r.etudiant_id }}</p>
                    </div>
                  </div>
                </td>
                <!-- Cours -->
                <td class="px-6 py-4 text-sm text-gray-600">{{ r.nomCours }}</td>
                <!-- Date -->
                <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(r.heure_pointage) }}</td>
                <!-- Heure -->
                <td class="px-6 py-4 text-sm text-gray-600">{{ formatHeure(r.heure_pointage) }}</td>
                <!-- Méthode -->
                <td class="px-6 py-4">
                  <span v-if="r.methode_pointage?.toLowerCase().includes('visage') || r.methode_pointage?.toLowerCase().includes('facial')"
                    class="inline-flex items-center gap-1 text-xs font-medium bg-teal-50 text-teal-700 px-2 py-0.5 rounded-full">
                    <ScanLine class="w-3 h-3" /> Visage
                  </span>
                  <span v-else-if="r.methode_pointage?.toLowerCase().includes('scan') || r.methode_pointage?.toLowerCase().includes('qr')"
                    class="inline-flex items-center gap-1 text-xs font-medium bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full">
                    <QrCode class="w-3 h-3" /> {{ r.methode_pointage }}
                  </span>
                  <span v-else-if="r.methode_pointage"
                    class="inline-flex items-center gap-1 text-xs font-medium bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full">
                    <PenLine class="w-3 h-3" /> {{ r.methode_pointage }}
                  </span>
                  <span v-else class="text-xs text-gray-400">—</span>
                </td>
                <!-- Statut -->
                <td class="px-6 py-4">
                  <span :class="r.statut === 'Présent' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ r.statut === 'Présent' ? '✓ Présent' : '✗ ' + r.statut }}
                  </span>
                </td>
              </tr>

              <tr v-if="historiqueFiltré.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-400 text-sm">
                  Aucun enregistrement trouvé
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between px-6 py-4 border-t border-gray-100 bg-gray-50">
          <p class="text-sm text-gray-500">{{ historiqueFiltré.length }} enregistrements</p>
          <div class="flex items-center gap-2">
            <button @click="page--" :disabled="page <= 1"
              class="px-3 py-1.5 text-sm text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed">
              ← Précédent
            </button>
            <span class="text-sm text-gray-500">{{ page }} / {{ totalPages }}</span>
            <button @click="page++" :disabled="page >= totalPages"
              class="px-3 py-1.5 text-sm text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed">
              Suivant →
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Search, Download, QrCode, PenLine, ScanLine, Loader2, AlertCircle } from 'lucide-vue-next'
import api from '@/services/api'

// ─── État ───────────────────────────────────────────────
const chargement = ref(true)
const erreur = ref(null)
const recherche = ref('')
const filtreCours = ref(null)
const filtreStatut = ref('')
const page = ref(1)
const PAR_PAGE = 15

const listePresences = ref([])
const listeEtudiants = ref([])
const listeSeances = ref([])
const listeCours = ref([])

// Reset page quand les filtres changent
watch([recherche, filtreCours, filtreStatut], () => { page.value = 1 })

// ─── Données enrichies (jointure client-side) ────────────
const historiqueEnrichi = computed(() =>
  listePresences.value.map(p => {
    const etudiant = listeEtudiants.value.find(e => e.id === p.etudiant_id) ?? null
    const seance   = listeSeances.value.find(s => s.id === p.seance_id) ?? null
    const cours    = seance ? listeCours.value.find(c => c.id === seance.cours_id) : null
    return { ...p, etudiant, seance, nomCours: cours?.nom ?? '—', coursId: seance?.cours_id ?? null }
  })
)

const historiqueFiltré = computed(() =>
  historiqueEnrichi.value.filter(r => {
    const texte = `${r.etudiant?.prenom ?? ''} ${r.etudiant?.nom ?? ''} ${r.etudiant?.matricule ?? ''}`.toLowerCase()
    const okRech   = !recherche.value   || texte.includes(recherche.value.toLowerCase())
    const okCours  = !filtreCours.value || r.coursId === filtreCours.value
    const okStatut = !filtreStatut.value || r.statut === filtreStatut.value
    return okRech && okCours && okStatut
  })
)

const totalPages   = computed(() => Math.max(1, Math.ceil(historiqueFiltré.value.length / PAR_PAGE)))
const historiquePagine = computed(() => {
  const debut = (page.value - 1) * PAR_PAGE
  return historiqueFiltré.value.slice(debut, debut + PAR_PAGE)
})

// ─── Chargement ──────────────────────────────────────────
const chargerDonnees = async () => {
  chargement.value = true
  erreur.value = null
  try {
    const [resP, resE, resS, resC] = await Promise.all([
      api.get('/presences/?limit=1000'),
      api.get('/etudiants/?limit=1000'),
      api.get('/seances/?limit=1000'),
      api.get('/cours/mes-cours'),
    ])
    listePresences.value = resP.data
    listeEtudiants.value = resE.data
    listeSeances.value   = resS.data
    listeCours.value     = resC.data
  } catch (e) {
    erreur.value = e.response?.data?.detail ?? 'Impossible de charger les données.'
    console.error('Historique :', e)
  } finally {
    chargement.value = false
  }
}

// ─── Helpers ─────────────────────────────────────────────
const formatDate = d => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const formatHeure = d => d
  ? new Date(d).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  : '—'

// ─── Export CSV ──────────────────────────────────────────
const exporterCSV = () => {
  const entetes = ['Prénom', 'Nom', 'Matricule', 'Cours', 'Date', 'Heure', 'Méthode', 'Statut']
  const lignes = historiqueFiltré.value.map(r => [
    r.etudiant?.prenom ?? '',
    r.etudiant?.nom ?? '',
    r.etudiant?.matricule ?? '',
    r.nomCours,
    formatDate(r.heure_pointage),
    formatHeure(r.heure_pointage),
    r.methode_pointage ?? '',
    r.statut,
  ])
  const csv  = [entetes, ...lignes].map(l => l.map(v => `"${v}"`).join(';')).join('\n')
  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href = url; a.download = 'historique_presences.csv'; a.click()
  URL.revokeObjectURL(url)
}

onMounted(chargerDonnees)
</script>