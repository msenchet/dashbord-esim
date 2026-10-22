/**
 * Permet de déposer un fichier n'importe où sur la page pour l'importer
 * (un cadre en pointillés apparaît pendant le survol).
 */
function bindDragAndDrop() {
  addEventListener("dragenter", e => {
    if (!e.dataTransfer.types.includes("Files")) return;
    dragDepth++;
    document.body.classList.add("dragging");
  });
  addEventListener("dragleave", () => {
    if (--dragDepth > 0) return;
    dragDepth = 0;
    document.body.classList.remove("dragging");
  });
  addEventListener("dragover", e => e.preventDefault());
  addEventListener("drop", e => {
    e.preventDefault();
    dragDepth = 0;
    document.body.classList.remove("dragging");
    if (e.dataTransfer.files.length) importFiles(e.dataTransfer.files);
  });
}
