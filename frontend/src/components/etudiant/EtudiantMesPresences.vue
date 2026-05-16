<template>
  <div>
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900">Mes Présences</h2>
      <p class="text-sm text-gray-500 mt-1">Suivi de votre assiduité par matière</p>
    </div>

    <div v-if="chargement" class="flex items-center justify-center py-24 text-gray-400">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
      Chargement de vos présences...
    </div>

    <template v-else>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 text-center">
          <p class="text-3xl font-bold text-green-600">{{ stats.tauxGlobal }}%</p>
          <p class="text-sm text-gray-500 mt-1">Taux global de présence</p>
        </div>
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 text-center">
          <p class="text-3xl font-bold text-gray-900">{{ stats.totalPresences }}</p>
          <p class="text-sm text-gray-500 mt-1">Séances suivies</p>
        </div>
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 text-center">
          <p class="text-3xl font-bold text-red-500">{{ stats.totalAbsences }}</p>
          <p class="text-sm text-gray-500 mt-1">Absences (séances ratées)</p>
        </div>
      </div>

      <div>
        <h3 class="text-base font-semibold text-gray-900 mb-4">Historique détaillé</h3>
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Matière</th>
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Heure du Scan</th>
                  <th class="text-left px-6 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Statut</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="p in presencesDetaillees" :key="p.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-3 text-sm text-gray-600">{{ p.date }}</td>
                  <td class="px-6 py-3 text-sm font-medium text-gray-900">{{ p.matiere }}</td>
                  <td class="px-6 py-3 text-sm text-gray-500">{{ p.creneau }}</td>
                  <td class="px-6 py-3">
                    <span :class="p.present ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ p.present ? '✓ Présent' : '✗ Absent' }}
                    </span>
                  </td>
                </tr>
                <tr v-if="presencesDetaillees.length === 0">
                  <td colspan="4" class="px-6 py-8 text-center text-gray-500 text-sm">Aucune présence enregistrée.</td>
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
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const presencesDetaillees = ref([])
const stats = ref({ tauxGlobal: 0, totalPresences: 0, totalAbsences: 0 })
const chargement = ref(true)

const chargerMesPresences = async () => {
  try {
    const [resPresences, resSeances, resCours, resStats] = await Promise.all([
      api.get('/presences/mes-presences'),
      api.get('/seances/mon-emploi-du-temps'), // <-- On charge SES séances
      api.get('/cours/?limit=1000'),
      api.get('/dashboard/stats/etudiant')
    ])

    stats.value.tauxGlobal    = resStats.data.tauxDePresence ?? 0
    stats.value.totalAbsences = Math.round((resStats.data.heuresAbsence ?? 0) / 2)
    stats.value.totalPresences = resPresences.data.length

    const maintenant = new Date()

    // On crée l'historique à partir des SÉANCES PASSÉES, pas juste des présences !
    const historique = []
    
    resSeances.data.forEach(seance => {
      const dateFin = new Date(seance.date_heure_fin)
      
      // Si la séance est terminée
      if (dateFin < maintenant) {
        const cours = resCours.data.find(c => c.id === seance.cours_id)
        // On cherche s'il a pointé à cette séance
        const presence = resPresences.data.find(p => p.seance_id === seance.id)
        
        historique.push({
          id: seance.id,
          matiere: cours ? cours.nom : 'Cours inconnu',
          date: new Date(seance.date_heure_debut).toLocaleDateString('fr-FR'),
          creneau: new Date(seance.date_heure_debut).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }),
          present: !!presence // true s'il a pointé, false sinon
        })
      }
    })

    // On trie du plus récent au plus ancien
    presencesDetaillees.value = historique.sort((a, b) => new Date(b.date) - new Date(a.date))

  } catch (error) {
    console.error('Erreur chargement présences :', error)
  } finally {
    chargement.value = false
  }
}

onMounted(chargerMesPresences)
</script>