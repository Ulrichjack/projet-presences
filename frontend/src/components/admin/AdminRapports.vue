<template>
  <div>
    <!-- ══ EN-TÊTE ══ -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Rapports & Exports</h2>
        <p class="text-sm text-gray-500 mt-1">
          Système de suivi biométrique · {{ totalEnregistrements }} enregistrements au total
        </p>
      </div>

      <!-- Boutons export -->
      <div class="flex flex-wrap gap-3">
        <button @click="exporter('csv')" :disabled="chargement || !historiqueFiltré.length"
          class="inline-flex items-center gap-2 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors disabled:opacity-40 shadow-sm">
          <FileText class="w-4 h-4 text-gray-500" /> CSV
        </button>
        <button @click="exporter('excel')" :disabled="chargement || !historiqueFiltré.length"
          class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors disabled:opacity-40 shadow-sm">
          <Table2 class="w-4 h-4" /> Excel
        </button>
        <button @click="exporter('pdf')" :disabled="chargement || !historiqueFiltré.length"
          class="inline-flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors disabled:opacity-40 shadow-sm">
          <FileDown class="w-4 h-4" /> PDF
        </button>
      </div>
    </div>

    <!-- ══ CARTES RÉSUMÉ SYSTÈME ══ -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-8">
      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Total présences</p>
        <p class="text-3xl font-bold text-gray-900">{{ resumeSysteme.totalPresences }}</p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Total absences</p>
        <p class="text-3xl font-bold text-red-600">{{ resumeSysteme.totalAbsences }}</p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Taux moyen</p>
        <p class="text-3xl font-bold" :class="resumeSysteme.tauxMoyen >= 75 ? 'text-green-600' : 'text-orange-500'">
          {{ resumeSysteme.tauxMoyen }}%
        </p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
        <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Cours couverts</p>
        <p class="text-3xl font-bold text-blue-600">{{ listeCours.length }}</p>
      </div>
    </div>

    <!-- ══ CHARGEMENT ══ -->
    <div v-if="chargement" class="flex items-center justify-center py-24 text-gray-400 gap-3">
      <div class="animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
      <span class="font-medium">Chargement des données système...</span>
    </div>

    <template v-else>
      <!-- ══ PANNEAU FILTRES ══ -->
      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm mb-6">
        <div class="flex items-center gap-2 mb-4">
          <div class="w-1 h-5 bg-blue-600 rounded-full"></div>
          <h3 class="text-sm font-bold text-gray-900 uppercase tracking-widest">Filtres du rapport</h3>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input v-model="recherche" type="text" placeholder="Nom, matricule..."
              class="w-full pl-9 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors" />
          </div>

          <select v-model="filtreCours"
            class="bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
            <option :value="null">Tous les cours</option>
            <option v-for="c in listeCours" :key="c.id" :value="c.id">{{ c.nom }}</option>
          </select>

          <select v-model="filtreStatut"
            class="bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
            <option value="">Tous les statuts</option>
            <option value="Présent">Présents uniquement</option>
            <option value="Absent">Absents uniquement</option>
          </select>

          <div class="flex gap-2">
            <input v-model="filtreDateDebut" type="date" title="Date début"
              class="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors" />
            <input v-model="filtreDateFin" type="date" title="Date fin"
              class="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors" />
          </div>
        </div>

        <div class="mt-4 flex items-center gap-3">
          <span class="text-xs font-semibold text-blue-700 bg-blue-50 px-3 py-1 rounded-full">
            {{ historiqueFiltré.length }} enregistrements sélectionnés
          </span>
          <button v-if="aDesFilteres" @click="reinitialiserFiltres"
            class="text-xs text-gray-500 hover:text-gray-900 underline transition-colors">
            Effacer les filtres
          </button>
        </div>
      </div>

      <!-- ══ TABLEAU ══ -->
      <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-100">
                <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Étudiant</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Cours</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Heure</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Méthode</th>
                <th class="text-center px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Statut</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="(r, index) in historiquePaginé" :key="r.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
                      :class="r.statut === 'Présent' ? 'bg-blue-600' : 'bg-gray-400'">
                      {{ r.etudiant ? (r.etudiant.prenom[0] + r.etudiant.nom[0]).toUpperCase() : '??' }}
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ r.etudiant?.prenom }} {{ r.etudiant?.nom }}</p>
                      <p class="text-xs text-gray-500 font-mono">{{ r.etudiant?.matricule ?? 'ID:' + r.etudiant_id }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm font-medium text-gray-700">{{ r.nomCours }}</td>
                <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(r.heure_pointage) }}</td>
                <td class="px-6 py-4">
                  <span class="text-sm font-semibold text-gray-700 bg-gray-100 px-2 py-1 rounded-lg">
                    {{ formatHeure(r.heure_pointage) }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full"
                    :class="badgeMethode(r.methode_pointage).classe">
                    <component :is="badgeMethode(r.methode_pointage).icone" class="w-3.5 h-3.5" />
                    {{ badgeMethode(r.methode_pointage).label }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span class="inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-full"
                    :class="r.statut === 'Présent' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                    {{ r.statut }}
                  </span>
                </td>
              </tr>
              <tr v-if="historiqueFiltré.length === 0">
                <td colspan="6" class="py-16 text-center">
                  <div class="flex flex-col items-center gap-3 text-gray-400">
                    <FileText class="w-10 h-10 opacity-50" />
                    <p class="font-medium text-gray-500">Aucun enregistrement trouvé</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex flex-col sm:flex-row items-center justify-between gap-3 px-6 py-4 bg-gray-50 border-t border-gray-100">
          <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Page {{ page }} sur {{ totalPages }}
          </p>
          <div class="flex items-center gap-2">
            <button @click="page--" :disabled="page <= 1"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all">
              Précédent
            </button>
            <button @click="page++" :disabled="page >= totalPages"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all">
              Suivant
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Search, FileText, FileDown, Table2, QrCode, ScanLine, PenLine } from 'lucide-vue-next'
import api from '@/services/api'
import { exporterCSV, exporterExcel, exporterPDF, formaterLignePresence } from '@/composables/useExport'

// ─── État ───────────────────────────────────────────────
const chargement      = ref(true)
const recherche       = ref('')
const filtreCours     = ref(null)
const filtreStatut    = ref('')
const filtreDateDebut = ref('')
const filtreDateFin   = ref('')
const page            = ref(1)
const PAR_PAGE        = 20

const listePresences  = ref([])
const listeEtudiants  = ref([])
const listeSeances    = ref([])
const listeCours      = ref([])

watch([recherche, filtreCours, filtreStatut, filtreDateDebut, filtreDateFin], () => { page.value = 1 })

// ─── Données enrichies ───────────────────────────────────
const historiqueEnrichi = computed(() =>
  listePresences.value.map(p => {
    const etudiant = listeEtudiants.value.find(e => e.id === p.etudiant_id) ?? null
    const seance   = listeSeances.value.find(s => s.id === p.seance_id)    ?? null
    const cours    = seance ? listeCours.value.find(c => c.id === seance.cours_id) : null
    return { ...p, etudiant, seance, nomCours: cours?.nom ?? '—', coursId: seance?.cours_id ?? null }
  })
)

const historiqueFiltré = computed(() =>
  historiqueEnrichi.value.filter(r => {
    const texte = `${r.etudiant?.prenom ?? ''} ${r.etudiant?.nom ?? ''} ${r.etudiant?.matricule ?? ''}`.toLowerCase()
    const ok1 = !recherche.value      || texte.includes(recherche.value.toLowerCase())
    const ok2 = !filtreCours.value    || r.coursId === filtreCours.value
    const ok3 = !filtreStatut.value   || r.statut === filtreStatut.value
    const ok4 = !filtreDateDebut.value || new Date(r.heure_pointage) >= new Date(filtreDateDebut.value)
    const ok5 = !filtreDateFin.value  || new Date(r.heure_pointage) <= new Date(filtreDateFin.value + 'T23:59:59')
    return ok1 && ok2 && ok3 && ok4 && ok5
  })
)

const totalPages = computed(() => Math.max(1, Math.ceil(historiqueFiltré.value.length / PAR_PAGE)))
const historiquePaginé = computed(() => {
  const debut = (page.value - 1) * PAR_PAGE
  return historiqueFiltré.value.slice(debut, debut + PAR_PAGE)
})

// ─── Statistiques résumé ─────────────────────────────────
const totalEnregistrements = computed(() => listePresences.value.length)
const resumeSysteme = computed(() => {
  const total    = historiqueEnrichi.value.length
  const presents = historiqueEnrichi.value.filter(r => r.statut === 'Présent').length
  const absents  = total - presents
  return {
    totalPresences: presents,
    totalAbsences:  absents,
    tauxMoyen:      total > 0 ? Math.round((presents / total) * 100) : 0
  }
})

const aDesFilteres = computed(() =>
  recherche.value || filtreCours.value || filtreStatut.value || filtreDateDebut.value || filtreDateFin.value
)

const reinitialiserFiltres = () => {
  recherche.value = ''; filtreCours.value = null; filtreStatut.value = ''
  filtreDateDebut.value = ''; filtreDateFin.value = ''
}

// ─── Chargement ──────────────────────────────────────────
const chargerDonnees = async () => {
  chargement.value = true
  try {
    const [resP, resE, resS, resC] = await Promise.all([
      api.get('/presences/?limit=5000'),
      api.get('/etudiants/?limit=5000'),
      api.get('/seances/?limit=5000'),
      api.get('/cours/?limit=500'),
    ])
    listePresences.value = resP.data
    listeEtudiants.value = resE.data
    listeSeances.value   = resS.data
    listeCours.value     = resC.data
  } catch (e) {
    console.error('AdminRapports :', e)
  } finally {
    chargement.value = false
  }
}

// ─── Export ──────────────────────────────────────────────
const nomFichier = (ext) => {
  const d = new Date().toLocaleDateString('fr-FR').replace(/\//g, '-')
  return `rapport_presences_${d}.${ext}`
}

const donneesFormatees = () => historiqueFiltré.value.map(formaterLignePresence)

const exporter = async (format) => {
  const data = donneesFormatees()
  if (format === 'csv')   return exporterCSV(data, nomFichier('csv'))
  if (format === 'excel') return exporterExcel(data, nomFichier('xlsx'), 'Présences')
  if (format === 'pdf') {
    const colonnes = [
      { header: 'Prénom',    dataKey: 'Prénom' },
      { header: 'Nom',       dataKey: 'Nom' },
      { header: 'Matricule', dataKey: 'Matricule' },
      { header: 'Cours',     dataKey: 'Cours' },
      { header: 'Date',      dataKey: 'Date' },
      { header: 'Heure',     dataKey: 'Heure' },
      { header: 'Méthode',   dataKey: 'Méthode' },
      { header: 'Statut',    dataKey: 'Statut' },
    ]
    return exporterPDF(data, nomFichier('pdf'), {
      titre:      'Rapport Global des Présences',
      sousTitre:  `${data.length} enregistrements · Généré le ${new Date().toLocaleDateString('fr-FR')}`,
      colonnes,
      orientation: 'landscape',
      ecole:      'PresencePro – Suivi biométrique QR Code & Reconnaissance Faciale',
    })
  }
}

// ─── Helpers ─────────────────────────────────────────────
const formatDate  = d => d ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
const formatHeure = d => d ? new Date(d).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '—'

const badgeMethode = (m) => {
  if (!m) return { label: '—', classe: 'bg-gray-100 text-gray-600', icone: PenLine }
  const ml = m.toLowerCase()
  if (ml.includes('visage') || ml.includes('facial'))
    return { label: 'Visage',  classe: 'bg-purple-100 text-purple-700', icone: ScanLine }
  if (ml.includes('qr') || ml.includes('scan'))
    return { label: 'QR Code', classe: 'bg-blue-100 text-blue-700', icone: QrCode }
  return { label: m, classe: 'bg-gray-100 text-gray-600', icone: PenLine }
}

onMounted(chargerDonnees)
</script>