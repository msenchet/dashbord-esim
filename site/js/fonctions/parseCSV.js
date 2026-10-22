/**
 * Lit un texte CSV (guillemets et retours à la ligne gérés) en liste d'objets.
 * @param {string} text contenu du fichier
 * @returns {Object[]} une ligne par objet, clés = en-têtes ; lignes vides ignorées
 */
function parseCSV(text) {
  const delim = detectDelimiter(text.split(/\r?\n/, 1)[0]);
  // rows : lignes lues ; row/field : ligne et champ en cours ; quoted : entre guillemets.
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === delim) { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows.filter(r => r.some(v => v.trim() !== ""));
  return head ? body.map(r => Object.fromEntries(head.map((h, i) => [h, r[i] ?? ""]))) : [];
}
