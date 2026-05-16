/**
 * useExport.js
 * Composable Vue 3 – Export CSV / Excel / PDF
 */

// ─────────────────────────────────────────────
// 1. EXPORT CSV
// ─────────────────────────────────────────────
export const exporterCSV = (donnees, nomFichier = 'export.csv') => {
  if (!donnees.length) return

  const entetes = Object.keys(donnees[0])
  const lignes  = donnees.map(row =>
    entetes.map(k => `"${(row[k] ?? '').toString().replace(/"/g, '""')}"`).join(';')
  )
  const csv  = [entetes.join(';'), ...lignes].join('\n')
  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' })
  telecharger(blob, nomFichier)
}

// ─────────────────────────────────────────────
// 2. EXPORT EXCEL
// ─────────────────────────────────────────────
export const exporterExcel = async (donnees, nomFichier = 'export.xlsx', titreOnglet = 'Présences') => {
  if (!donnees.length) return

  const XLSX = await import('xlsx')
  const ws = XLSX.utils.json_to_sheet(donnees)

  const cols = Object.keys(donnees[0]).map(k => ({
    wch: Math.max(k.length, ...donnees.map(r => String(r[k] ?? '').length)) + 2
  }))
  ws['!cols'] = cols

  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, titreOnglet)
  XLSX.writeFile(wb, nomFichier)
}

// ─────────────────────────────────────────────
// 3. EXPORT PDF (CORRIGÉ ✅)
// ─────────────────────────────────────────────
export const exporterPDF = async (donnees, nomFichier = 'rapport.pdf', options = {}) => {
  if (!donnees.length) return

  // Import dynamique
  const { jsPDF } = await import('jspdf')
  const autoTableModule = await import('jspdf-autotable')
  
  // Gère la différence d'import selon la version de Vite/Rollup
  const autoTable = autoTableModule.default || autoTableModule

  const {
    titre     = 'Rapport de Présences',
    sousTitre = `Généré le ${new Date().toLocaleDateString('fr-FR')}`,
    colonnes  = null,
    orientation = 'landscape',
    ecole     = 'PresencePro – Système de suivi biométrique',
  } = options

  const doc = new jsPDF({ orientation, unit: 'mm', format: 'a4' })
  const pageW = doc.internal.pageSize.getWidth()

  // ── En-tête ──
  doc.setFillColor(0, 0, 0)
  doc.rect(0, 0, pageW, 22, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text(titre, 14, 10)
  doc.setFontSize(8)
  doc.setFont('helvetica', 'normal')
  doc.text(sousTitre, 14, 16)
  doc.text(ecole, pageW - 14, 16, { align: 'right' })

  // ── Tableau ──
  const entetes = colonnes ?? Object.keys(donnees[0]).map(k => ({ header: k, dataKey: k }))

  // ✅ CORRECTION ICI : On utilise autoTable comme une fonction autonome !
  autoTable(doc, {
    startY: 28,
    head: [entetes.map(c => c.header)],
    body: donnees.map(row => entetes.map(c => row[c.dataKey] ?? '—')),
    styles: {
      fontSize: 8,
      cellPadding: 3,
      textColor: [30, 30, 30],
      lineColor: [200, 200, 200],
      lineWidth: 0.2,
    },
    headStyles: {
      fillColor: [30, 30, 30],
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      fontSize: 8,
    },
    alternateRowStyles: { fillColor: [248, 248, 248] },
    didDrawPage: (data) => {
      const total = doc.internal.getNumberOfPages()
      doc.setFontSize(7)
      doc.setTextColor(150)
      doc.text(
        `Page ${data.pageNumber} / ${total}  –  ${donnees.length} enregistrements`,
        pageW / 2,
        doc.internal.pageSize.getHeight() - 6,
        { align: 'center' }
      )
    },
  })

  doc.save(nomFichier)
}

// ─────────────────────────────────────────────
// Utilitaire interne
// ─────────────────────────────────────────────
const telecharger = (blob, nomFichier) => {
  const url = URL.createObjectURL(blob)
  const a   = document.createElement('a')
  a.href = url
  a.download = nomFichier
  a.click()
  URL.revokeObjectURL(url)
}

export const formaterLignePresence = (p) => ({
  'Prénom':    p.etudiant?.prenom    ?? '—',
  'Nom':       p.etudiant?.nom       ?? '—',
  'Matricule': p.etudiant?.matricule ?? '—',
  'Cours':     p.nomCours            ?? '—',
  'Date':      p.heure_pointage
    ? new Date(p.heure_pointage).toLocaleDateString('fr-FR')
    : '—',
  'Heure':     p.heure_pointage
    ? new Date(p.heure_pointage).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    : '—',
  'Méthode':   p.methode_pointage    ?? '—',
  'Statut':    p.statut              ?? '—',
})