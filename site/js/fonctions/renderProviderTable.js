/**
 * Affiche le tableau « Répartition par fournisseur » (fournisseur cliquable).
 * @param {Object[]} prov lignes par fournisseur (voir byProvider)
 */
function renderProviderTable(prov) {
  const head = `<thead><tr><th>Fournisseur</th><th class="num">Offres</th>
    <th class="num">Part</th><th class="num">Prix moyen</th><th class="num">Prix min</th>
    <th class="num">Prix max</th><th class="num">Illimitées</th><th class="num">€/Go</th>
    </tr></thead>`;
  const body = prov.map(p => `<tr><td>${cellPick("provider", p, esc(p.provider))}</td>
      <td class="num">${fmtInt(p.count)}</td>
      <td class="num">${p.share.toLocaleString("fr-FR",
        { minimumFractionDigits: 1, maximumFractionDigits: 1 })} %</td>
      <td class="num">${fmtEur(p.mean)}</td><td class="num">${fmtEur(p.min)}</td>
      <td class="num">${fmtEur(p.max)}</td><td class="num">${p.unlimited}</td>
      <td class="num">${p.perGb === null ? "—" : fmtEur(p.perGb)}</td></tr>`).join("");
  document.getElementById("t-providers").innerHTML = head + "<tbody>" + body + "</tbody>";
}
