/**
 * Importe des fichiers choisis ou déposés (CSV, JSON ou TXT).
 * @param {FileList|File[]} fileList fichiers sélectionnés
 */
async function importFiles(fileList) {
  const files = [...fileList].filter(f =>
    /\.(csv|json|txt)$/i.test(f.name) || /csv|json/.test(f.type));
  if (!files.length) return setStatus("Formats acceptés : .csv ou .json", "error");
  setStatus("Lecture des fichiers…");
  try {
    const sources = await Promise.all(files.map(async f => [await f.text(), f.name]));
    ingest(sources, files.map(f => f.name).join(", "));
  } catch (e) {
    setStatus(`Import impossible : ${e.message}`, "error");
  }
}
