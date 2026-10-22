/**
 * Lit, nettoie et fusionne des contenus importés, puis rafraîchit toute la page.
 * @param {Array} sources liste de [texte, nom de fichier]
 * @param {string} label nom de la source affiché
 * @throws {Error} si un contenu est illisible ou ne contient aucune offre valide
 */
function ingest(sources, label) {
  // rowCount : lignes lues ; notes : avertissements (API paginée par exemple).
  let rowCount = 0;
  const notes = [];
  const incoming = sources.flatMap(([text, name]) => {
    const { records, total } = readAny(text, name);
    rowCount += records.length;
    if (total && total > records.length) {
      notes.push(`l'API annonce ${fmtInt(total)} offres mais n'en a renvoyé que `
        + `${fmtInt(records.length)} (pagination : augmente le paramètre limit)`);
    }
    try { return cleanRecords(records, name); }
    catch (e) { throw new Error(`${name} : ${e.message}`); }
  });
  if (!incoming.length) throw new Error("aucune offre valide trouvée (prix manquant ou illisible)");
  const { added, updated } = mergeDataset(incoming, label);
  refreshControls();
  update();
  renderSource();
  const ignored = rowCount - incoming.length;
  const n = incoming.length;
  setStatus(`${label} : ${fmtInt(n)} offre${plural(n)} importée${plural(n)} `
    + `(${fmtInt(added)} ajoutée${plural(added)}, ${fmtInt(updated)} mise${plural(updated)} à jour)`
    + (ignored ? ` · ${fmtInt(ignored)} lignes ignorées (prix illisible ou doublon)` : "")
    + (notes.length ? ` · ⚠ ${notes.join(" ; ")}` : ""), "ok");
}
