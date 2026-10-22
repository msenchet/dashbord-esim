/**
 * Ferme le résumé avec le bouton ✕ ou un clic sur le fond assombri (Échap est natif).
 */
function bindSummaryClose() {
  document.getElementById("sum-close").addEventListener("click", () => summaryEl.close());
  summaryEl.addEventListener("click", e => {
    if (e.target === summaryEl) summaryEl.close();
  });
}
