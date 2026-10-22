/**
 * Importe le contenu d'une URL (API JSON ou fichier CSV en ligne).
 * L'API doit être joignable depuis le navigateur et autoriser CORS.
 * @param {string} url adresse à charger
 */
async function importUrl(url) {
  if (!url) {
    return setStatus("Indique l'URL d'une API (JSON) ou d'un fichier CSV en ligne.", "error");
  }
  setStatus("Chargement depuis l'API…");
  try {
    let response;
    try { response = await fetch(url); }
    catch (e) {
      throw new Error("requête bloquée. L'API doit être joignable depuis ce navigateur, en HTTPS, "
        + "et autoriser CORS (en-tête Access-Control-Allow-Origin).");
    }
    if (!response.ok) throw new Error(`l'API a répondu ${response.status} ${response.statusText}`);
    // name : nom de fichier déduit de l'URL, « .json » ajouté si le serveur annonce du JSON.
    const address = new URL(url, location.href);
    let name = address.pathname.split("/").pop() || address.hostname;
    const isJson = (response.headers.get("content-type") || "").includes("json");
    if (isJson && !/\.json$/i.test(name)) name += ".json";
    ingest([[await response.text(), name]], address.href);
  } catch (e) {
    setStatus(`Import impossible : ${e.message}`, "error");
  }
}
