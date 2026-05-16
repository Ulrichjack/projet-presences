<template>
  <div>
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Gestion du Personnel (Profs & Admins)</h2>
        <p class="text-sm text-gray-500 mt-1">{{ enseignants.length }} membres enregistrés</p>
      </div>
      <button @click="ouvrirModal()" class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2.5 rounded-xl shadow-sm transition-colors duration-200">
        <UserPlus class="w-4 h-4" />
        Ajouter un membre
      </button>
    </div>

    <!-- Barre de recherche + filtre -->
    <div class="flex flex-col sm:flex-row gap-3 mb-5">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input v-model="recherche" type="text" placeholder="Rechercher par nom, email..." class="w-full pl-9 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <select v-model="filtreRole" class="bg-white border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="">Tous les rôles</option>
        <option value="ADMIN">Admin</option>
        <option value="PROF">Professeur</option>
      </select>
    </div>

    <!-- Tableau -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-100 bg-gray-50">
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">ID</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Nom complet</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Spécialité</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Rôle</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="u in enseignantsFiltres" :key="u.id" class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-4 text-sm text-gray-400 font-mono">#{{ u.id }}</td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-semibold flex-shrink-0">
                    {{ u.prenom[0] }}{{ u.nom[0] }}
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ u.prenom }} {{ u.nom }}</p>
                    <p class="text-xs text-gray-500">{{ u.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ u.specialite || '—' }}</td>
              <td class="px-6 py-4">
                <span :class="u.role === 'ADMIN' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ u.role }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button @click="ouvrirModal(u)" class="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">Modifier</button>
                  <button @click="confirmerSuppression(u)" class="text-sm font-medium text-red-500 hover:text-red-700 transition-colors">Supprimer</button>
                </div>
              </td>
            </tr>
            <tr v-if="enseignantsFiltres.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-400 text-sm">Aucun membre trouvé</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODALE Ajouter / Modifier -->
    <Teleport to="body">
      <div v-if="modalOuverte" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" @click.self="fermerModal">
        <div class="bg-white w-full max-w-md rounded-2xl shadow-2xl">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">{{ modeEdition ? 'Modifier le membre' : 'Nouveau membre' }}</h3>
            <button @click="fermerModal" class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"><X class="w-5 h-5 text-gray-500" /></button>
          </div>
          <form @submit.prevent="sauvegarder" class="px-6 py-5 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Prénom</label>
                <input v-model="form.prenom" type="text" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Nom</label>
                <input v-model="form.nom" type="text" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Email</label>
              <input v-model="form.email" type="email" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Rôle</label>
                <select v-model="form.role" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                  <option value="PROF">Professeur</option>
                  <option value="ADMIN">Administrateur</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Matricule</label>
                <input v-model="form.matricule" type="text" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Spécialité (Optionnel)</label>
              <input v-model="form.specialite" type="text" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div v-if="!modeEdition">
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Mot de passe</label>
              <input v-model="form.mot_de_passe" type="password" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
              <button type="button" @click="fermerModal" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100">Annuler</button>
              <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm">Enregistrer</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODALE Suppression -->
    <Teleport to="body">
      <div v-if="modalSuppressionOuverte" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="bg-white w-full max-w-sm rounded-2xl shadow-2xl p-6 text-center">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4"><Trash2 class="w-6 h-6 text-red-600" /></div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Supprimer le membre ?</h3>
          <p class="text-sm text-gray-500 mb-6">Le membre <strong>{{ enseignantASupprimer?.prenom }} {{ enseignantASupprimer?.nom }}</strong> sera définitivement supprimé.</p>
          <div class="flex gap-3 justify-center">
            <button @click="modalSuppressionOuverte = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100">Annuler</button>
            <button @click="supprimerEnseignant" class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-xl">Oui, supprimer</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, UserPlus, X, Trash2 } from 'lucide-vue-next'
import api from '@/services/api'

const enseignants = ref([])
const recherche = ref('')
const filtreRole = ref('')
const modalOuverte = ref(false)
const modalSuppressionOuverte = ref(false)
const modeEdition = ref(false)
const enseignantASupprimer = ref(null)

const form = ref({ id: null, nom: '', prenom: '', matricule: '', email: '', mot_de_passe: '', specialite: '', role: 'PROF' })

const enseignantsFiltres = computed(() => {
  return enseignants.value.filter(e => {
    const matchRecherche = `${e.prenom} ${e.nom} ${e.email}`.toLowerCase().includes(recherche.value.toLowerCase())
    const matchRole = filtreRole.value === '' || e.role === filtreRole.value
    return matchRecherche && matchRole
  })
})

const chargerEnseignants = async () => {
  try {
    const response = await api.get('/enseignants/')
    enseignants.value = response.data
  } catch (error) { console.error("Erreur:", error) }
}

const sauvegarder = async () => {
  try {
    if (modeEdition.value) {
      await api.put(`/enseignants/${form.value.id}`, form.value)
    } else {
      await api.post('/enseignants/', form.value)
    }
    fermerModal()
    chargerEnseignants()
  } catch (error) { alert(error.response?.data?.detail || "Erreur de sauvegarde") }
}

const supprimerEnseignant = async () => {
  try {
    await api.delete(`/enseignants/${enseignantASupprimer.value.id}`)
    modalSuppressionOuverte.value = false
    chargerEnseignants()
  } catch (error) { alert("Erreur de suppression") }
}

const ouvrirModal = (e = null) => {
  modeEdition.value = !!e
  form.value = e ? { ...e, mot_de_passe: '' } : { id: null, nom: '', prenom: '', matricule: '', email: '', mot_de_passe: '', specialite: '', role: 'PROF' }
  modalOuverte.value = true
}

const fermerModal = () => { modalOuverte.value = false }
const confirmerSuppression = (e) => { enseignantASupprimer.value = e; modalSuppressionOuverte.value = true }

onMounted(chargerEnseignants)
</script>