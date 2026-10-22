/**
 * Met à jour le sous-titre et la ligne « source » du panneau Données ;
 * le bouton « Données d'origine » n'apparaît qu'après un import.
 */
function renderSource() {
  const providers = new Set(OFFERS.map(o => o.provider)).size;
  document.getElementById("subtitle").textContent =
    `${fmtInt(OFFERS.length)} offres de ${providers} fournisseurs · prix en EUR`;
  document.getElementById("source-info").textContent =
    `${fmtInt(OFFERS.length)} offres · ${providers} fournisseurs · source : ${SOURCES.join(" + ")}`;
  document.getElementById("restore").hidden = OFFERS === BASE;
}
