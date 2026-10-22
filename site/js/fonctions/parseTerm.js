/**
 * Interprète un mot de la recherche : mot-clé (« illimité », « 5g »), comparaison numérique
 * (« <20€ », « >=5go », « 10-30€ », « 30j ») ou simple texte.
 * Sans unité ni préfixe, un nombre avec opérateur est un prix ; un nombre seul reste du texte.
 * @param {string} word mot normalisé
 * @returns {{label: string, test: Function}} libellé affiché et test appliqué à une offre
 */
function parseTerm(word) {
  const keyword = KEYWORDS[word];
  if (keyword) return { label: keyword.label, test: o => norm(o[keyword.field]) === keyword.value };
  const match = word.match(TERM_RE);
  if (!match) return textTerm(word);
  const [, prefix, op, low, high, unit] = match;
  if ((prefix && !PREFIX_FIELD[prefix]) || (unit && !UNIT_FIELD[unit])) return textTerm(word);
  const field = PREFIX_FIELD[prefix] || UNIT_FIELD[unit] || (op || high ? "price" : null);
  if (!field) return textTerm(word);
  // factor : conversion des Mo en Go ; lo / hi : bornes numériques tapées.
  const factor = unit === "mo" ? 0.001 : 1;
  const lo = toNum(low) * factor;
  const hi = high === undefined ? null : toNum(high) * factor;
  const [name, suffix] = FIELD_LABEL[field];
  if (hi !== null) {
    return { label: `${name} ${fmtNum(lo)} – ${fmtNum(hi)}${suffix}`,
      test: o => o[field] !== null && o[field] >= lo && o[field] <= hi };
  }
  // « 20€ » sans opérateur = budget maximum ; « 5go » ou « 30j » = valeur exacte.
  const operator = op || (field === "price" ? "<=" : "=");
  return { label: `${name} ${OP_LABEL[operator]} ${fmtNum(lo)}${suffix}`,
    test: o => o[field] !== null && compareValues(operator, o[field], lo) };
}
