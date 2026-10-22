/**
 * Affiche un message sous le panneau d'import.
 * @param {string} message texte affiché
 * @param {string} [kind="info"] « info », « ok » (préfixe ✓) ou « error » (préfixe ⚠)
 */
function setStatus(message, kind = "info") {
  const prefix = kind === "error" ? "⚠ " : kind === "ok" ? "✓ " : "";
  statusEl.textContent = prefix + message;
  statusEl.dataset.kind = kind;
}
