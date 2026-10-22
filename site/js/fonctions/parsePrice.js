/**
 * Convertit un prix écrit librement en nombre : « 12,45 € », « 1 234,50 », 12.45 → 12.45.
 * @param {*} value prix brut
 * @returns {number} le prix, NaN s'il est illisible
 */
function parsePrice(value) {
  if (typeof value === "number") return value;
  if (isBlank(value)) return NaN;
  // text : prix sans espaces ni symbole monétaire.
  let text = String(value).replace(/[\s ]/g, "").replace(/[^\d,.\-]/g, "");
  if (text.includes(",") && text.includes(".")) {
    // Les deux séparateurs sont présents : le dernier est le séparateur décimal.
    text = text.lastIndexOf(",") > text.lastIndexOf(".")
      ? text.replace(/\./g, "").replace(",", ".")
      : text.replace(/,/g, "");
  } else {
    text = text.replace(/,/g, ".");
  }
  return text === "" ? NaN : Number(text);
}
