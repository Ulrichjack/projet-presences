<template>
  <div>
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Gestion des Étudiants</h2>
        <p class="text-sm text-gray-500 mt-1">{{ etudiants.length }} étudiants enregistrés</p>
      </div>
      <button @click="ouvrirModal()" class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2.5 rounded-xl shadow-sm transition-colors duration-200">
        <UserPlus class="w-4 h-4" />
        Ajouter un étudiant
      </button>
    </div>

    <!-- Barre de recherche -->
    <div class="flex flex-col sm:flex-row gap-3 mb-5">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input v-model="recherche" type="text" placeholder="Rechercher par nom, matricule, email..." class="w-full pl-9 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
    </div>

    <!-- Tableau -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-100 bg-gray-50">
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">ID</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Nom complet</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Matricule</th>
              <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Email</th>
              <th class="text-right px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="e in etudiantsFiltres" :key="e.id" class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-4 text-sm text-gray-400 font-mono">#{{ e.id }}</td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white text-xs font-semibold flex-shrink-0">
                    {{ e.prenom[0] }}{{ e.nom[0] }}
                  </div>
                  <p class="text-sm font-medium text-gray-900">{{ e.prenom }} {{ e.nom }}</p>
                </div>
              </td>
              <td class="px-6 py-4 text-sm font-semibold text-gray-700">{{ e.matricule }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ e.email }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button @click="ouvrirModal(e)" class="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">Modifier</button>
                  <button @click="confirmerSuppression(e)" class="text-sm font-medium text-red-500 hover:text-red-700 transition-colors">Supprimer</button>
                </div>
              </td>
            </tr>
            <tr v-if="etudiantsFiltres.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-400 text-sm">Aucun étudiant trouvé</td>
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
            <h3 class="text-lg font-semibold text-gray-900">{{ modeEdition ? 'Modifier l\'étudiant' : 'Nouvel étudiant' }}</h3>
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
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Matricule</label>
              <input v-model="form.matricule" type="text" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Email</label>
              <input v-model="form.email" type="email" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div v-if="!modeEdition">
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Mot de passe</label>
              <input v-model="form.mot_de_passe" type="password" required class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Photo pour l'IA (Visage)</label>
              <input type="file" @change="handleFileUpload" accept="image/*" required
                class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
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
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Supprimer l'étudiant ?</h3>
          <p class="text-sm text-gray-500 mb-6">L'étudiant <strong>{{ etudiantASupprimer?.prenom }} {{ etudiantASupprimer?.nom }}</strong> sera définitivement supprimé.</p>
          <div class="flex gap-3 justify-center">
            <button @click="modalSuppressionOuverte = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-100">Annuler</button>
            <button @click="supprimerEtudiant" class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-xl">Oui, supprimer</button>
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

const etudiants = ref([])
const recherche = ref('')
const modalOuverte = ref(false)
const modalSuppressionOuverte = ref(false)
const modeEdition = ref(false)
const etudiantASupprimer = ref(null)

const form = ref({ id: null, nom: '', prenom: '', matricule: '', email: '', mot_de_passe: '', qr_code: '' })

const etudiantsFiltres = computed(() => {
  return etudiants.value.filter(e => `${e.prenom} ${e.nom} ${e.matricule} ${e.email}`.toLowerCase().includes(recherche.value.toLowerCase()))
})

const chargerEtudiants = async () => {
  try {
    const response = await api.get('/etudiants/')
    etudiants.value = response.data
  } catch (error) { console.error("Erreur:", error) }
}

const selectedFile = ref(null)

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0]
}

const sauvegarder = async () => {
  try {
    if (modeEdition.value) {
      // -------------------------------------------------
      // 1. MODE MODIFICATION (PUT) -> On envoie du JSON
      // -------------------------------------------------
      const payload = {
        nom: form.value.nom,
        prenom: form.value.prenom,
        matricule: form.value.matricule,
        email: form.value.email,
        qr_code: form.value.qr_code || `QR-${form.value.matricule}`
      }
      
      // On ajoute le mot de passe UNIQUEMENT si l'admin en a tapé un nouveau
      if (form.value.mot_de_passe && form.value.mot_de_passe.trim() !== '') {
        payload.mot_de_passe = form.value.mot_de_passe
      }

      await api.put(`/etudiants/${form.value.id}`, payload)

    } else {
      // -------------------------------------------------
      // 2. MODE CRÉATION (POST) -> On envoie FormData (fichier)
      // -------------------------------------------------
      const fd = new FormData()
      fd.append('nom', form.value.nom)
      fd.append('prenom', form.value.prenom)
      fd.append('matricule', form.value.matricule)
      fd.append('email', form.value.email)
      fd.append('mot_de_passe', form.value.mot_de_passe)
      fd.append('qr_code', form.value.qr_code || `QR-${form.value.matricule}`)
      
      if (selectedFile.value) {
        fd.append('photo', selectedFile.value)
      } else {
        alert("La photo est obligatoire pour la reconnaissance faciale")
        return
      }

      await api.post('/etudiants/', fd)
    }

    // Si ça réussit, on ferme et on actualise la liste
    fermerModal()
    chargerEtudiants()

  } catch (error) {
    alert(error.response?.data?.detail || "Erreur lors de la sauvegarde")
  }
}

const supprimerEtudiant = async () => {
  try {
    await api.delete(`/etudiants/${etudiantASupprimer.value.id}`)
    modalSuppressionOuverte.value = false
    chargerEtudiants()
  } catch (error) { alert("Erreur de suppression") }
}

const ouvrirModal = (e = null) => {
  modeEdition.value = !!e
  form.value = e ? { ...e, mot_de_passe: '' } : { id: null, nom: '', prenom: '', matricule: '', email: '', mot_de_passe: '', qr_code: '' }
  modalOuverte.value = true
}

const fermerModal = () => { modalOuverte.value = false }
const confirmerSuppression = (e) => { etudiantASupprimer.value = e; modalSuppressionOuverte.value = true }

onMounted(chargerEtudiants)
</script>