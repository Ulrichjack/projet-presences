<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <!-- Mobile Menu Overlay -->
    <div
      v-if="isMobileMenuOpen"
      class="fixed inset-0 bg-black/50 z-40 lg:hidden"
      @click="isMobileMenuOpen = false"
    />

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-0 left-0 z-50 h-full w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out lg:translate-x-0',
        isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-6 py-5 border-b border-gray-100">
        <div class="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
          <CheckCircle class="w-6 h-6 text-white" />
        </div>
        <div>
          <span class="text-lg font-semibold text-gray-900">Présence</span>
          <span class="text-lg font-semibold text-blue-600">Pro</span>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="px-4 py-6">
        <ul class="space-y-1">
          <li v-for="item in navigationItems" :key="item.name">
            <button
              @click="activeNav = item.name; isMobileMenuOpen = false"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200',
                activeNav === item.name
                  ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600 -ml-1 pl-5'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              ]"
            >
              <component :is="item.icon" class="w-5 h-5" />
              {{ item.label }}
            </button>
          </li>
        </ul>

        <!-- Logout -->
        <div class="mt-8 pt-6 border-t border-gray-100">
          <button
            @click="handleLogout"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-gray-600 hover:bg-red-50 hover:text-red-600 transition-all duration-200"
          >
            <LogOut class="w-5 h-5" />
            Déconnexion
          </button>
        </div>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="lg:ml-64">
      <!-- Header -->
      <header class="sticky top-0 z-30 bg-white border-b border-gray-200">
        <div class="flex items-center justify-between px-4 lg:px-8 py-4">
          <button
            @click="isMobileMenuOpen = true"
            class="lg:hidden p-2 -ml-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Menu class="w-6 h-6" />
          </button>

                    <!-- On n'affiche le titre global QUE si on est sur la page d'accueil -->
          <h1 v-if="activeNav === 'Tableau de bord'" class="text-xl lg:text-2xl font-semibold text-gray-900">
            {{ pageTitle }}
          </h1>
          <div v-else></div> <!-- Espace vide pour garder la mise en page -->

          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
              <div class="hidden sm:block text-right">
                <p class="text-sm font-medium text-gray-900">{{ utilisateur.prenom }} {{ utilisateur.nom }}</p>
                <p class="text-xs text-gray-500">{{ utilisateur.role }}</p>
              </div>
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
                {{ getInitials(utilisateur.prenom, utilisateur.nom) }}
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- ✅ ZONE PRINCIPALE : CONTENU DYNAMIQUE -->
      <main class="p-4 lg:p-8">

        <!-- ==========================================
             TABLEAU DE BORD (accueil selon le rôle)
             ========================================== -->
        <template v-if="activeNav === 'Tableau de bord'">

          <!-- Stats Admin -->
                    <!-- Stats Admin -->
          <div v-if="utilisateur.role === 'ADMIN'">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-8">
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Total Étudiants</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalEtudiants || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Total Professeurs</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalProfesseurs || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Taux de Présence Global</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.tauxDePresence || 0 }}%</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Séances du jour</p>
                <p class="text-3xl font-bold text-indigo-600 mt-2">{{ stats.seancesDuJour || 0 }}</p>
              </div>
            </div>

            <!-- NOUVEAU : ACTIVITÉ RÉCENTE -->
            <h3 class="text-lg font-bold text-gray-900 mb-4">Cours récemment ajoutés</h3>
            <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
              <table class="w-full text-left text-sm">
                <thead class="bg-gray-50 border-b border-gray-100 text-gray-500">
                  <tr>
                    <th class="px-6 py-3 font-semibold">Code</th>
                    <th class="px-6 py-3 font-semibold">Nom du cours</th>
                    <th class="px-6 py-3 font-semibold">Filière</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="c in stats.derniersCours" :key="c.id" class="hover:bg-gray-50">
                    <td class="px-6 py-3 font-mono text-blue-600">{{ c.code }}</td>
                    <td class="px-6 py-3 font-medium text-gray-900">{{ c.nom }}</td>
                    <td class="px-6 py-3 text-gray-500">{{ c.filiere }}</td>
                  </tr>
                  <tr v-if="!stats.derniersCours || stats.derniersCours.length === 0">
                    <td colspan="3" class="px-6 py-8 text-center text-gray-400">Aucun cours récent</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

                    <!-- ==========================================
               Stats Professeur
               ========================================== -->
          <div v-else-if="utilisateur.role === 'PROF'">
            <!-- 1. La grille pour les 3 cartes en haut -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6 mb-8">
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Mes Cours</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.profCours || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <p class="text-sm font-medium text-gray-500">Total de mes Séances</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.profSeances || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm border-l-4 border-red-500">
                <p class="text-sm font-medium text-gray-500">Étudiants à risque</p>
                <p class="text-3xl font-bold text-red-600 mt-2">{{ stats.profRisque || 0 }}</p>
              </div>
            </div>

            <!-- 2. Le tableau en dessous (en dehors de la grille !) -->
            <h3 class="text-lg font-bold text-gray-900 mb-4 mt-8">Mes Cours Assignés</h3>
            <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden mb-8">
              <table class="w-full text-left text-sm">
                <thead class="bg-gray-50 border-b border-gray-100 text-gray-500">
                  <tr>
                    <th class="px-6 py-3 font-semibold">Code</th>
                    <th class="px-6 py-3 font-semibold">Nom du cours</th>
                    <th class="px-6 py-3 font-semibold">Filière</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="c in stats.mesCoursList" :key="c.id" class="hover:bg-gray-50">
                    <td class="px-6 py-3 font-mono text-blue-600">{{ c.code }}</td>
                    <td class="px-6 py-3 font-medium text-gray-900">{{ c.nom }}</td>
                    <td class="px-6 py-3 text-gray-500">{{ c.filiere }}</td>
                  </tr>
                  <tr v-if="!stats.mesCoursList || stats.mesCoursList.length === 0">
                    <td colspan="3" class="px-6 py-8 text-center text-gray-400">Vous n'avez aucun cours assigné.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- ==========================================
               Stats Étudiant
               ========================================== -->
          <div v-else>
            <!-- 1. La grille pour les 3 cartes en haut -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 lg:gap-6 mb-8">
              <div class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
                <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Mon Taux de Présence</p>
                <p class="text-4xl font-black text-green-600 mt-2">{{ stats.tauxDePresence || 0 }}%</p>
              </div>
              <div class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
                <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Heures d'Absence</p>
                <p class="text-4xl font-black text-red-600 mt-2">{{ stats.heuresAbsence || 0 }} h</p>
              </div>
              <!-- <div class="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-6 shadow-md text-white">
                <p class="text-sm font-medium text-blue-100 uppercase tracking-wider">Prochain Cours</p>
                <p class="text-2xl font-bold mt-2">{{ stats.prochainCours || '...' }}</p>
              </div> -->
            </div>

            <!-- 2. La bannière en dessous (en dehors de la grille !) -->
            <h3 class="text-lg font-bold text-gray-900 mb-4 mt-8">Action Rapide</h3>
            <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex items-center justify-between">
              <div>
                <p class="font-semibold text-gray-900">Le cours va commencer ?</p>
                <p class="text-sm text-gray-500">Ouvrez la caméra pour scanner le QR Code du tableau.</p>
              </div>
              <button @click="activeNav = 'ScannerEtudiant'" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium shadow-sm transition-colors flex items-center gap-2">
                <Camera class="w-5 h-5" /> Lancer le Scanner
              </button>
            </div>
          </div>

        </template>

        <!-- ==========================================
             PAGES ADMIN
             ========================================== -->
        <AdminEtudiants   v-else-if="activeNav === 'Etudiants'" />
        <AdminEnseignants v-else-if="activeNav === 'Enseignants'" />
        <AdminCours       v-else-if="activeNav === 'Cours'" />
        <AdminSeances     v-else-if="activeNav === 'Seances'" />
        <AdminInscriptions v-else-if="activeNav === 'Inscriptions'" />
        <AdminRapports     v-else-if="activeNav === 'Rapports'" /> 
        <ProfScanner      v-else-if="activeNav === 'Scanner'" />
        <!-- ==========================================
             PAGES PROFESSEUR
             ========================================== -->
        <ProfMesCours     v-else-if="activeNav === 'Mes Cours'" />
        <ProfMesSeances   
          v-else-if="activeNav === 'Mes Seances'" 
          @aller-scanner="activeNav = 'Scanner'" 
        />        
        <ProfScanner      v-else-if="activeNav === 'Scanner'" />
        <ProfHistorique   v-else-if="activeNav === 'Historique'" />

        <!-- ==========================================
             PAGES ÉTUDIANT
             ========================================== -->
        <EtudiantEmploiDuTemps v-else-if="activeNav === 'Emploi du temps'" />
        <EtudiantMesPresences  v-else-if="activeNav === 'Mes Presences'" />
        <EtudiantMonQR         v-else-if="activeNav === 'Mon QR'" />
        <EtudiantScanner       v-else-if="activeNav === 'ScannerEtudiant'" /> <!-- 👈 AJOUT ICI -->


      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted , watch} from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import {
  Home, BookOpen, Users, Camera, QrCode, LogOut,
  Menu, Calendar, CheckCircle, ClipboardList, UserCheck,FileText 
} from 'lucide-vue-next'

// ✅ Import des composants de pages
import AdminEtudiants    from '@/components/admin/AdminEtudiants.vue'
import AdminEnseignants  from '@/components/admin/AdminEnseignants.vue'
import AdminCours        from '@/components/admin/AdminCours.vue'
import AdminSeances      from '@/components/admin/AdminSeances.vue'
import AdminInscriptions from '@/components/admin/AdminInscriptions.vue'
import AdminRapports from '@/components/admin/AdminRapports.vue' 

import ProfMesCours      from '@/components/prof/ProfMesCours.vue'
import ProfMesSeances    from '@/components/prof/ProfMesSeances.vue'
import ProfScanner       from '@/components/prof/ProfScanner.vue'
import ProfHistorique    from '@/components/prof/ProfHistorique.vue'

import EtudiantEmploiDuTemps from '@/components/etudiant/EtudiantEmploiDuTemps.vue'
import EtudiantMesPresences  from '@/components/etudiant/EtudiantMesPresences.vue'
import EtudiantMonQR         from '@/components/etudiant/EtudiantMonQR.vue'
import EtudiantScanner from '@/components/etudiant/EtudiantScanner.vue'
// --- INIT ---
const router = useRouter()
const authStore = useAuthStore()
const utilisateur = ref({ email: '', role: '...', id: null, prenom: '', nom: '' })
const isMobileMenuOpen = ref(false)
const activeNav = ref(localStorage.getItem('pageActive') || 'Tableau de bord')
const stats = ref({ totalEtudiants: 0, seancesDuJour: 0, tauxDePresence: 0 })


watch(activeNav, (nouvellePage) => {
  localStorage.setItem('pageActive', nouvellePage)
})
// --- MÉTHODES ---
const handleLogout = () => { 
  authStore.deconnexion();
  localStorage.removeItem('pageActive')
   router.push('/') 
  }

const getInitials = (prenom, nom) => {
  if (!prenom && !nom) return '??'
  return `${(prenom || '')[0] || ''}${(nom || '')[0] || ''}`.toUpperCase()
}

const chargerStats = async () => {
  try {
    if (utilisateur.value.role === 'ETUDIANT') {
      const response = await api.get('/dashboard/stats/etudiant')
      stats.value = { ...stats.value, ...response.data }
    } 
    else if (utilisateur.value.role === 'PROF') {
      // ✅ On charge les données du prof
      const resCours = await api.get('/cours/mes-cours')
      const resSeances = await api.get('/seances/mes-seances')
      
      // ✅ On recrée tout l'objet pour forcer Vue.js à mettre à jour l'écran !
      stats.value = {
        ...stats.value,
        profCours: resCours.data.length,
        profSeances: resSeances.data.length,
        profRisque: 0, // (On met 0 par défaut pour le moment)
        mesCoursList: resCours.data 
      }
    }
    else {
      // ADMIN
      const response = await api.get('/dashboard/stats')
      stats.value = { ...stats.value, ...response.data }
    }
  } catch (error) {
    console.error("Erreur de chargement des stats:", error)
  }
}

onMounted(() => {
  if (!authStore.estConnecte) { router.push('/'); return }
  try {
    const payload = JSON.parse(atob(authStore.token.split('.')[1]))
    utilisateur.value = { email: payload.sub, role: payload.role, id: payload.id, prenom: payload.prenom || '', nom: payload.nom || '' }
  } catch (e) { handleLogout() }
  chargerStats()
})

// --- COMPUTED ---
const pageTitle = computed(() => {
  const labels = {
    'Tableau de bord': 'Tableau de bord',
    'Utilisateurs': 'Gestion des Utilisateurs',
    'Cours': 'Gestion des Cours',
    'Seances': 'Toutes les Séances',
    'Mes Cours': 'Mes Cours',
    'Mes Seances': 'Mes Séances',
    'Scanner': 'Scanner – Faire l\'appel',
    'Historique': 'Historique des Appels',
    'Emploi du temps': 'Mon Emploi du Temps',
    'Mes Presences': 'Mes Présences',
    'Mon QR': 'Mon QR Code',
  }
  return labels[activeNav.value] || activeNav.value
})

const navigationItems = computed(() => {
  if (utilisateur.value.role === 'ADMIN') {
    return [
      { name: 'Tableau de bord', label: 'Tableau de bord', icon: Home },
      { name: 'Etudiants', label: 'Gestion Étudiants', icon: Users }, // <-- NOUVEAU
      { name: 'Enseignants', label: 'Gestion Enseignants', icon: Users },      { name: 'Cours', label: 'Gestion des Cours', icon: BookOpen },
      { name: 'Seances', label: 'Toutes les Séances', icon: Calendar },
      { name: 'Inscriptions', label: 'Inscriptions aux cours', icon: UserCheck },
      { name: 'Rapports', label: 'Rapports & Exports', icon: FileText }, // 👈 AJOUT ICI
      { name: 'Scanner', label: 'Scanner (Caméra)', icon: Camera }, // 👈 AJOUTE CETTE LIGNE

    ]
  } else if (utilisateur.value.role === 'PROF') {
    return [
      { name: 'Tableau de bord', label: 'Tableau de bord', icon: Home },
      { name: 'Mes Cours', label: 'Mes Cours', icon: BookOpen },
      { name: 'Mes Seances', label: 'Mes Séances', icon: Calendar },
      { name: 'Scanner', label: 'Scanner (Caméra)', icon: Camera },
      { name: 'Historique', label: 'Historique des appels', icon: ClipboardList },
    ]
  } else {
    return [
      { name: 'Tableau de bord', label: 'Tableau de bord', icon: Home },
      { name: 'Emploi du temps', label: 'Mon Emploi du temps', icon: Calendar },
      { name: 'Mes Presences', label: 'Mes Présences', icon: UserCheck },
      { name: 'Mon QR', label: 'Mon QR Code', icon: QrCode },
      { name: 'ScannerEtudiant', label: 'Scanner la classe', icon: Camera }, // 👈 AJOUT ICI

    ]
  }
})
</script>

<style>
html { font-family: 'Inter', system-ui, sans-serif; }
</style>