/**
 * Met à jour le filtre de prix à chaque saisie (un champ vidé reprend sa borne par défaut).
 */
function bindPriceInputs() {
  [pminEl, pmaxEl].forEach(input => input.addEventListener("input", () => {
    state.pmin = pminEl.value === "" ? priceMin : Number(pminEl.value);
    state.pmax = pmaxEl.value === "" ? priceMax : Number(pmaxEl.value);
    update();
  }));
}
