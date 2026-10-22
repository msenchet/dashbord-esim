/**
 * Remplace les pastilles proposées.
 * @param {Object} ctrl contrôle créé par createChips
 * @param {Array} options liste de [valeur, libellé]
 */
function setChipOptions(ctrl, options) {
  ctrl.root.innerHTML = options.map(([value, label]) =>
    `<button class="chip" type="button" data-v="${esc(value)}">${esc(label)}</button>`).join("");
  syncChips(ctrl);
}
