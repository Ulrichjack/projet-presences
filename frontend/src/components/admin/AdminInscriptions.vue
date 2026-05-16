<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Inscriptions aux Cours</h2>
        <p class="text-sm text-gray-500 mt-1">Liez les étudiants aux matières</p>
      </div>
      <button @click="ouvrirModal()" class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2.5 rounded-xl shadow-sm transition-all">
        <Plus class="w-4 h-4" /> Inscrire un étudiant
      </button>
    </div>

    <!-- Tableau des Inscriptions -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Étudiant</th>
            <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Cours</th>
            <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Date d'inscription</th>
            <th class="px-6 py-4 text-right text-xs font-bold text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="ins in inscriptions" :key="ins.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ getNomEtudiant(ins.etudiant_id) }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ getNomCours(ins.cours_id) }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(ins.date_inscription).toLocaleDateString() }}</td>
            <td class="px-6 py-4 text-right">
              <button @click="supprimer(ins.id)" class="text-red-500 hover:text-red-700 text-sm font-bold">Désinscrire</button>
            </td>
          </tr>
          <tr v-if="inscriptions.length === 0">
            <td colspan="4" class="px-6 py-10 text-center text-gray-400">Aucune inscription enregistrée.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODALE INSCRIPTION -->
    <div v-if="showModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
        <h3 class="text-xl font-bold mb-6">Nouvelle Inscription</h3>
        <form @submit.prevent="sauvegarder" class="space-y-4">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">Choisir l'étudiant</label>
            <select v-model="form.etudiant_id" required class="w-full p-3 bg-gray-50 border rounded-xl outline-none focus:ring-2 focus:ring-blue-500">
              <option v-for="e in etudiants" :key="e.id" :value="e.id">{{ e.prenom }} {{ e.nom }} ({{ e.matricule }})</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">Choisir le cours</label>
            <select v-model="form.cours_id" required class="w-full p-3 bg-gray-50 border rounded-xl outline-none focus:ring-2 focus:ring-blue-500">
              <option v-for="c in cours" :key="c.id" :value="c.id">{{ c.nom }}</option>
            </select>
          </div>
          <div class="flex gap-3 pt-4">
            <button type="button" @click="showModal = false" class="flex-1 py-3 bg-gray-100 rounded-xl font-bold">Annuler</button>
            <button type="submit" class="flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold shadow-md">Valider</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from 'lucide-vue-next'
import api from '@/services/api'

const inscriptions = ref([])
const etudiants = ref([])
const cours = ref([])
const showModal = ref(false)
const form = ref({ etudiant_id: '', cours_id: '' })

const chargerDonnees = async () => {
  try {
    const [resI, resE, resC] = await Promise.all([
      api.get('/inscriptions/'),
      api.get('/etudiants/'),
      api.get('/cours/')
    ])
    inscriptions.value = resI.data
    etudiants.value = resE.data
    cours.value = resC.data
  } catch (e) { console.error(e) }
}

const getNomEtudiant = (id) => {
  const e = etudiants.value.find(x => x.id === id)
  return e ? `${e.prenom} ${e.nom}` : 'Inconnu'
}

const getNomCours = (id) => cours.value.find(x => x.id === id)?.nom || 'Inconnu'

const ouvrirModal = () => { showModal.value = true }

const sauvegarder = async () => {
  try {
    await api.post('/inscriptions/', form.value)
    showModal.value = false
    chargerDonnees()
  } catch (e) { alert(e.response?.data?.detail || "Erreur") }
}

const supprimer = async (id) => {
  if (confirm("Désinscrire cet étudiant ?")) {
    await api.delete(`/inscriptions/${id}`)
    chargerDonnees()
  }
}

onMounted(chargerDonnees)
</script>