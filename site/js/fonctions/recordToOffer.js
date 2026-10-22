/**
 * Transforme une ligne importée normalisée en offre (mêmes règles que esim/clean_offers.py).
 * @param {Object} r ligne normalisée (voir normalizeRecord)
 * @param {string} fallback fournisseur par défaut (déduit du nom de fichier)
 * @returns {Object|null} l'offre, ou null si le prix est illisible
 */
function recordToOffer(r, fallback) {
  const price = parsePrice(r.price);
  if (!Number.isFinite(price)) return null;
  let [gb, unlimited] = parseData(r.data_gb, recordText(r, "data_display"));
  if (TRUE_WORDS.includes(String(r.is_unlimited ?? "").trim().toLowerCase())) unlimited = true;
  // validityMatch : premier nombre de la validité (« 30 jours » → 30).
  const validityMatch = String(r.validity_days ?? "").match(/\d+/);
  const validity = validityMatch ? Number(validityMatch[0]) : null;
  const provider = recordText(r, "provider") || fallback;
  const country = recordText(r, "country_name") || "Inconnu";
  const display = unlimited ? "Illimité"
    : (recordText(r, "data_display") || (gb === null ? "N/C" : gb + " Go"));
  const name = recordText(r, "product_name")
    || `eSIM ${country} ${display}${validity === null ? "" : ` ${validity} jours`}`;
  // sku : identifiant fourni, ou fabriqué à partir du fournisseur, du nom et du prix.
  const sku = recordText(r, "sku")
    || `${provider.toLowerCase().replace(/\W+/g, "-")}-${hash(name + "|" + price)}`;
  return makeOffer({
    sku, provider, country, code: recordText(r, "country_code"), name, gb, unlimited, display,
    validity, price, network: recordText(r, "network") || "N/C",
    topUp: TRUE_WORDS.includes(String(r.top_up ?? "").trim().toLowerCase()),
    currency: recordText(r, "currency") || "EUR",
  });
}
