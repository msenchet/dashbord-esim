/**
 * Affiche le tableau paginé « Toutes les offres » (en-têtes triables, flèche sur la colonne triée).
 * @param {Object[]} rows offres retenues par les filtres du haut
 */
function renderOffers(rows) {
  tableRows = searchRows(rows);
  const avgPerGb = computeStats(rows).price_per_gb_mean;
  const pages = Math.max(1, Math.ceil(tableRows.length / PAGE_SIZE));
  state.page = Math.min(state.page, pages - 1);
  const slice = tableRows.slice(state.page * PAGE_SIZE, (state.page + 1) * PAGE_SIZE);
  const head = OFFER_COLUMNS.map(c => {
    const arrow = state.sortKey === c.key ? (state.sortDir > 0 ? " ↑" : " ↓") : "";
    const align = c.numeric ? " num" : "";
    return `<th class="sortable${align}" data-k="${c.key}">${c.label}${arrow}</th>`;
  }).join("");
  const body = slice.length ? slice.map(o => offerRowHtml(o, avgPerGb)).join("")
    : `<tr><td colspan="9" class="empty">Aucune offre ne correspond à ces critères.</td></tr>`;
  document.getElementById("t-offers").innerHTML =
    `<thead><tr>${head}</tr></thead><tbody>${body}</tbody>`;
  document.getElementById("page-info").textContent =
    `${fmtInt(tableRows.length)} offres · page ${state.page + 1}/${pages}`;
  document.getElementById("prev").disabled = state.page === 0;
  document.getElementById("next").disabled = state.page >= pages - 1;
}
