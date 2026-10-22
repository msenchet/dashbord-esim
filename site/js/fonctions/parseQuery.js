/**
 * Découpe la recherche en critères : chaque mot doit être respecté (ET), une virgule donne
 * des alternatives (OU), « - » exclut, un texte entre guillemets est cherché tel quel.
 * Ex. : japon 5g <20€ >=5go 30j illimité -holafly "afrique du sud" japon,corée
 * @param {string} query texte tapé
 * @returns {Object[]} critères {raw, label, test}
 */
function parseQuery(query) {
  // prepared : « < 20 » devient « <20 » et « 20 € » devient « 20€ ».
  const prepared = query.replace(/(<=|>=|<|>|=)\s+/g, "$1")
    .replace(/(\d)\s+(€|eur|go|gb|mo|j|jours?)(?=[\s,]|$)/gi, "$1$2");
  return (prepared.match(TOKEN_RE) || []).map(raw => {
    const negated = raw.length > 1 && raw.startsWith("-");
    const body = negated ? raw.slice(1) : raw;
    const quoted = /^".*"$/.test(body);
    const alternatives = quoted ? [norm(body.slice(1, -1)).trim()]
      : norm(body).split(",").map(s => s.trim());
    const terms = alternatives.filter(Boolean).map(t => quoted ? textTerm(t) : parseTerm(t));
    if (!terms.length) return null;
    const label = (negated ? "sauf " : "") + terms.map(t => t.label).join(" ou ");
    return { raw, label, test: o => terms.some(t => t.test(o)) !== negated };
  }).filter(Boolean);
}
