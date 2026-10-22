/**
 * Branche le panneau « Données » : bouton d'import de fichier, formulaire d'URL,
 * bouton « Données d'origine ».
 */
function bindImportEvents() {
  document.getElementById("file-btn").addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => {
    importFiles(fileInput.files);
    fileInput.value = "";
  });
  document.getElementById("api-form").addEventListener("submit", e => {
    e.preventDefault();
    importUrl(document.getElementById("api-url").value.trim());
  });
  document.getElementById("restore").addEventListener("click", restoreOrigin);
}
