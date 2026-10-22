/**
 * Ouvre le panneau de résumé d'une sélection (fournisseur, tranche de prix, volume).
 * @param {Object} options
 * @param {string} options.kind type de sélection affiché au-dessus du titre
 * @param {string} options.title titre (nom du fournisseur, tranche…)
 * @param {Object[]} options.rows offres de la sélection
 * @param {string} options.groupBy « country » ou « provider » (liste des principaux)
 * @param {Object} options.list filtres appliqués par « Voir les offres » (voir showInList)
 * @param {Function} [options.global] action du bouton « Filtrer tout le dashboard »
 */
function openSummary({ kind, title, rows, groupBy, list, global }) {
  const s = computeStats(rows);
  const all = computeStats(current);
  document.getElementById("sum-kind").textContent = kind;
  document.getElementById("sum-title").textContent = title;
  document.getElementById("sum-sub").textContent =
    `${fmtInt(rows.length)} offre${plural(rows.length)}`
    + ` · ${pct(rows.length, current.length)} des offres affichées`;
  document.getElementById("sum-body").innerHTML =
    summaryBodyHtml(rows, groupBy, s, summaryDeltaHtml(s, all));
  const actions = document.getElementById("sum-actions");
  actions.innerHTML = `<button class="btn primary" type="button" data-act="list">`
    + `Voir les ${fmtInt(rows.length)} offres dans la liste ↓</button>`
    + (global ? `<button class="btn" type="button" data-act="global">`
      + "Filtrer tout le dashboard</button>" : "");
  actions.onclick = e => {
    const action = e.target.closest("[data-act]")?.dataset.act;
    if (action === "list") showInList(list);
    if (action === "global") { summaryEl.close(); global(); }
  };
  if (!summaryEl.open) summaryEl.showModal();
  document.getElementById("sum-body").scrollTop = 0;
}
