<template>
  <div>
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Toutes les Séances</h2>
        <p class="text-sm text-gray-500 mt-1">{{ seances.length }} séances planifiées</p>
      </div>
      <button @click="ouvrirModal()"
        class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2.5 rounded-xl shadow-sm transition-colors">
        <Plus class="w-4 h-4" />
        Planifier une séance
      </button>
    </div>

    <!-- Filtres -->
    <div class="flex flex-wrap gap-3 mb-5">
      <div class="relative flex-1 min-w-48">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input v-model="recherche" type="text" placeholder="Rechercher une salle..."
          class="w-full pl-9 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <select v-model="filtreCours"
        class="bg-white border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="">Tous les cours</option>
        <option v-for="c in listeCours" :key="c.id" :value="c.id">{{ c.nom }}</option>
      </select>
    </div>

    <!-- Tableau -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-100 bg-gray-50">
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Cours</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Professeur</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Date & Heure</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Salle</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Code Secret</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Statut</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="s in seancesFiltrees" :key="s.id" class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-4">
                <p class="text-sm font-medium text-gray-900">{{ getNomCours(s.cours_id) }}</p>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ getNomProf(s.enseignant_id) }}</td>
              <td class="px-6 py-4">
                <p class="text-sm text-gray-900">{{ formatDate(s.date_heure_debut) }}</p>
                <p class="text-xs text-gray-500">{{ formatHeure(s.date_heure_debut) }} – {{ formatHeure(s.date_heure_fin) }}</p>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ s.salle }}</td>
              <td class="px-6 py-4">
                <span class="font-mono text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded-lg font-bold">{{ s.code_validation }}</span>
              </td>
              <td class="px-6 py-4">
                <span :class="statutClass(s)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ getStatut(s) }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button @click="ouvrirModal(s)" class="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">Modifier</button>
                  <button @click="confirmerSuppression(s)" class="text-sm font-medium text-red-500 hover:text-red-700 transition-colors">Supprimer</button>
                </div>
              </td>
            </tr>
            <tr v-if="seancesFiltrees.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-400 text-sm">Aucune séance trouvée</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODALE Formulaire -->
    <Teleport to="body">
      <div v-if="modalOuverte" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="fermerModal">
        <div class="bg-white w-full max-w-lg rounded-2xl shadow-2xl">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">{{ modeEdition ? 'Modifier la séance' : 'Nouvelle séance' }}</h3>
            <button @click="fermerModal" class="p-1.5 hover:bg-gray-100 rounded-lg"><X class="w-5 h-5 text-gray-500" /></button>
          </div>
          <form @submit.prevent="sauvegarder" class="px-6 py-5 space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Cours</label>
              <select v-model="form.cours_id" required
                class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="" disabled>Sélectionner un cours</option>
                <option v-for="c in listeCours" :key="c.id" :value="c.id">{{ c.nom }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Professeur</label>
              <select v-model="form.enseignant_id" required
                class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="" disabled>Sélectionner un professeur</option>
                <option v-for="p in listeProfs" :key="p.id" :value="p.id">{{ p.prenom }} {{ p.nom }}</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Début</label>
                <input v-model="form.date_heure_debut" type="datetime-local" required
                  class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Fin</label>
                <input v-model="form.date_heure_fin" type="datetime-local" required
                  class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Salle</label>
              <input v-model="form.salle" type="text" placeholder="Ex: Amphi A" required
                class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
              <button type="button" @click="fermerModal" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Annuler</button>
              <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm transition-colors">
                {{ modeEdition ? 'Mettre à jour' : 'Enregistrer' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODALE Suppression -->
    <Teleport to="body">
      <div v-if="modalSuppressionOuverte" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="bg-white w-full max-w-sm rounded-2xl shadow-2xl p-6 text-center">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Trash2 class="w-6 h-6 text-red-600" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Supprimer la séance ?</h3>
          <p class="text-sm text-gray-500 mb-6">Cette séance sera définitivement supprimée.</p>
          <div class="flex gap-3 justify-center">
            <button @click="modalSuppressionOuverte = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Annuler</button>
            <button @click="supprimerSeance" class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-xl transition-colors">Oui, supprimer</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Plus, X, Trash2 } from 'lucide-vue-next'
import api from '@/services/api'

const seances = ref([])
const listeCours = ref([])
const listeProfs = ref([])

const recherche = ref('')
const filtreCours = ref('')
const modalOuverte = ref(false)
const modalSuppressionOuverte = ref(false)
const modeEdition = ref(false)
const seanceASupprimer = ref(null)

// Correspond au schéma SeanceCreate
const form = ref({ id: null, date_heure_debut: '', date_heure_fin: '', cours_id: '', enseignant_id: '', salle: '' })

// --- COMPUTED ---
const seancesFiltrees = computed(() => {
  return seances.value.filter(s => {
    const matchRech = s.salle.toLowerCase().includes(recherche.value.toLowerCase())
    const matchCours = filtreCours.value === '' || s.cours_id === filtreCours.value
    return matchRech && matchCours
  })
})

// --- API CALLS ---
const chargerDonnees = async () => {
  try {
    const [resSeances, resCours, resProfs] = await Promise.all([
      api.get('/seances/'),
      api.get('/cours/'),
      api.get('/enseignants/')
    ])
    seances.value = resSeances.data
    listeCours.value = resCours.data
    listeProfs.value = resProfs.data
  } catch (error) {
    console.error("Erreur de chargement:", error)
  }
}

const sauvegarder = async () => {
  try {
    // Les inputs datetime-local renvoient "YYYY-MM-DDTHH:mm", on ajoute ":00Z" pour FastAPI
    const payload = {
      cours_id: form.value.cours_id,
      enseignant_id: form.value.enseignant_id,
      salle: form.value.salle,
      date_heure_debut: new Date(form.value.date_heure_debut).toISOString(),
      date_heure_fin: new Date(form.value.date_heure_fin).toISOString()
    }

    if (modeEdition.value) {
      await api.put(`/seances/${form.value.id}`, payload)
    } else {
      await api.post('/seances/', payload)
    }
    fermerModal()
    chargerDonnees()
  } catch (error) {
    alert(error.response?.data?.detail || "Erreur de sauvegarde")
  }
}

const supprimerSeance = async () => {
  try {
    await api.delete(`/seances/${seanceASupprimer.value.id}`)
    modalSuppressionOuverte.value = false
    chargerDonnees()
  } catch (error) {
    alert("Erreur de suppression")
  }
}

// --- HELPERS ---
const getNomCours = (id) => listeCours.value.find(c => c.id === id)?.nom || 'Inconnu'
const getNomProf = (id) => {
  const p = listeProfs.value.find(p => p.id === id)
  return p ? `${p.prenom} ${p.nom}` : 'Inconnu'
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('fr-FR', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' })
const formatHeure = (dateStr) => new Date(dateStr).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })

// Calcule le statut en fonction de l'heure actuelle
const getStatut = (s) => {
  const now = new Date()
  const debut = new Date(s.date_heure_debut)
  const fin = new Date(s.date_heure_fin)
  
  if (now < debut) return 'PLANIFIÉE'
  if (now >= debut && now <= fin) return 'EN COURS'
  return 'TERMINÉE'
}

const statutClass = (s) => {
  const st = getStatut(s)
  if (st === 'EN COURS') return 'bg-blue-100 text-blue-700'
  if (st === 'TERMINÉE') return 'bg-gray-100 text-gray-700'
  return 'bg-yellow-100 text-yellow-700'
}

// Pour pré-remplir l'input datetime-local correctement
const toDateTimeLocal = (isoString) => {
  const date = new Date(isoString)
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  return date.toISOString().slice(0, 16)
}

const ouvrirModal = (s = null) => {
  modeEdition.value = !!s
  if (s) {
    form.value = {
      id: s.id,
      cours_id: s.cours_id,
      enseignant_id: s.enseignant_id,
      salle: s.salle,
      date_heure_debut: toDateTimeLocal(s.date_heure_debut),
      date_heure_fin: toDateTimeLocal(s.date_heure_fin)
    }
  } else {
    form.value = { id: null, cours_id: '', enseignant_id: '', salle: '', date_heure_debut: '', date_heure_fin: '' }
  }
  modalOuverte.value = true
}

const fermerModal = () => { modalOuverte.value = false }
const confirmerSuppression = (s) => { seanceASupprimer.value = s; modalSuppressionOuverte.value = true }

onMounted(chargerDonnees)
</script>