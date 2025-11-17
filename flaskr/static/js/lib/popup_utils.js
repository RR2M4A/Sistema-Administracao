// static/js/lib/popup_utils.js
"use strict"

export function activate_popup(popup, overlay, focus_element=null) {

    popup.style.display = "block";
    overlay.style.display = "block";

    if (focus_element) {
        focus_element.focus();
    }
}

export function deactivate_popup(popup, overlay, reset=true) {
    if (!popup) return;

    popup.style.display = "none";
    overlay.style.display = "none";

    if (reset) {
        reset_inputs(popup);
    }
}

export function reset_inputs(parent) {

    let inputs = parent.querySelectorAll('input');

    for (let input of inputs) {
        if (input.type != "radio") {
            input.value = "";
            input.removeAttribute("style");
        }
    }
}