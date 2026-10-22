/**
 * Affiche les pastilles des critères actifs (valeurs cliquées puis mots de la recherche),
 * chacune avec un ✕ pour la retirer, et un bouton « Tout effacer ».
 * @param {Object[]} criteria critères de la recherche (voir parseQuery)
 * @param {Array} picks couples [colonne, valeurs cliquées]
 */
function renderCriteria(criteria, picks) {
  const pickChips = picks.flatMap(([field, values]) => [...values].map(v =>
    `<button type="button" class="pick" data-f="${field}" data-v="${esc(v)}"
      aria-label="Retirer ${esc(PICK_FIELDS[field])} ${esc(pickLabel(field, v))}">
      ${esc(PICK_FIELDS[field])} : ${esc(pickLabel(field, v))} <span aria-hidden="true">✕</span>
    </button>`));
  const queryChips = criteria.map(c =>
    `<button type="button" class="pick query" data-raw="${esc(c.raw)}"
      aria-label="Retirer le critère ${esc(c.label)}">
      ${esc(c.label)} <span aria-hidden="true">✕</span></button>`);
  const chips = pickChips.concat(queryChips);
  const html = chips.length ? chips.join("")
    + `<button type="button" class="btn clear-picks" id="clear-picks">Tout effacer</button>` : "";
  if (html !== lastPicksHtml) {
    document.getElementById("picks").innerHTML = html;
    lastPicksHtml = html;
  }
}
