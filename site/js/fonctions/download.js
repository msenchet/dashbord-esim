/**
 * Fait télécharger un fichier généré dans le navigateur.
 * @param {string} filename nom proposé
 * @param {string} content contenu du fichier
 * @param {string} type type MIME (text/csv, application/json…)
 */
function download(filename, content, type) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const link = Object.assign(document.createElement("a"), { href: url, download: filename });
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
