<template>
  <div>
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Gestion des Cours</h2>
        <p class="text-sm text-gray-500 mt-1">{{ cours.length }} cours dans le programme</p>
      </div>
      <button @click="ouvrirModal()" class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2.5 rounded-xl shadow-sm transition-colors duration-200">
        <Plus class="w-4 h-4" />
        Ajouter un cours
      </button>
    </div>

    <!-- Barre de recherche -->
    <div class="flex flex-col sm:flex-row gap-3 mb-5">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input v-model="recherche" type="text" placeholder="Rechercher un cours..." class="w-full pl-9 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
    </div>

    <!-- Tableau -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-100 bg-gray-50">
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Code</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Nom du Cours</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Filière</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Niveau</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Crédits</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="c in coursFiltres" :key="c.id" class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-4">
                <span class="font-mono text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-lg font-semibold">{{ c.code }}</span>
              </td>
              <td class="px-6 py-4">
                <p class="text-sm font-medium text-gray-900">{{ c.nom }}</p>
                <p class="text-xs text-gray-400 mt-0.5 truncate max-w-xs">{{ c.description }}</p>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ c.filiere }}</td>
              <td class="px-6 py-4">
                <span class="text-xs font-medium bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full">{{ c.niveau }}</span>
              </td>
              <td class="px-6 py-4 text-sm font-semibold text-gray-700">{{ c.credits }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button @click="ouvrirModal(c)" class="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">Modifier</button>
                  <button @click="confirmerSuppression(c)" class="text-sm font-medium text-red-500 hover:text-red-700 transition-colors">Supprimer</button>
                </div>
              </td>
            </tr>
            <tr v-if="coursFiltres.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-400 text-sm">Aucun cours trouvé</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODALE Ajouter / Modifier -->
    <Teleport to="body">
      <div v-if="modalOuverte" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="fermerModal">
        <div class="bg-white w-full max-w-lg rounded-2xl shadow-2xl">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">{{ modeEdition ? 'Modifier le cours' : 'Nouveau cours' }}</h3>
            <button @click="fermerModal" class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors">
              <X class="w-5 h-5 text-gray-500" />
            </button>
          </div>
          <form @submit.prevent="sauvegarder" class="px-6 py-5 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Code du cours *</label>
                <input v-model="form.code" type="text" required placeholder="INFO301" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Crédits *</label>
                <input v-model.number="form.credits" type="number" min="1" required placeholder="3" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Nom du cours *</label>
              <input v-model="form.nom" type="text" required placeholder="Développement Web Avancé" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Description</label>
              <textarea v-model="form.description" rows="3" placeholder="Description du cours..." class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-none"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Filière *</label>
                <input v-model="form.filiere" type="text" required placeholder="Informatique" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Niveau *</label>
                <select v-model="form.niveau" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                  <option value="" disabled>Sélectionner</option>
                  <option value="L1">Licence 1</option>
                  <option value="L2">Licence 2</option>
                  <option value="L3">Licence 3</option>
                  <option value="M1">Master 1</option>
                  <option value="M2">Master 2</option>
                </select>
              </div>
            </div>
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
              <button type="button" @click="fermerModal" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Annuler</button>
              <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm transition-colors">Enregistrer</button>
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
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Supprimer le cours ?</h3>
          <p class="text-sm text-gray-500 mb-6">Le cours <strong>{{ coursASupprimer?.nom }}</strong> sera supprimé.</p>
          <div class="flex gap-3 justify-center">
            <button @click="modalSuppressionOuverte = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Annuler</button>
            <button @click="supprimerCours" class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-xl transition-colors">Oui, supprimer</button>
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

const cours = ref([])
const recherche = ref('')
const modalOuverte = ref(false)
const modalSuppressionOuverte = ref(false)
const modeEdition = ref(false)
const coursASupprimer = ref(null)

const form = ref({ id: null, nom: '', description: '', code: '', filiere: '', niveau: '', credits: 0 })

const coursFiltres = computed(() => {
  return cours.value.filter(c => c.nom.toLowerCase().includes(recherche.value.toLowerCase()))
})

const chargerCours = async () => {
  try {
    const response = await api.get('/cours/')
    cours.value = response.data
  } catch (error) { console.error("Erreur:", error) }
}

const sauvegarder = async () => {
  try {
    const payload = {
      nom: form.value.nom,
      description: form.value.description,
      code: form.value.code,
      filiere: form.value.filiere,
      niveau: form.value.niveau,
      credits: Number(form.value.credits)
    }
    if (modeEdition.value) {
      await api.put(`/cours/${form.value.id}`, payload)
    } else {
      await api.post('/cours/', payload)
    }
    fermerModal()
    chargerCours()
  } catch (error) { alert(error.response?.data?.detail || "Erreur") }
}

const supprimerCours = async () => {
  try {
    await api.delete(`/cours/${coursASupprimer.value.id}`)
    modalSuppressionOuverte.value = false
    chargerCours()
  } catch (error) { alert("Erreur de suppression") }
}

const ouvrirModal = (c = null) => {
  modeEdition.value = !!c
  form.value = c ? { ...c } : { id: null, nom: '', description: '', code: '', filiere: '', niveau: '', credits: 0 }
  modalOuverte.value = true
}

const fermerModal = () => { modalOuverte.value = false }
const confirmerSuppression = (c) => { coursASupprimer.value = c; modalSuppressionOuverte.value = true }

onMounted(chargerCours)
</script>