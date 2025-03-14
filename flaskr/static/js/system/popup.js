"use strict"

import { make_request } from "../utils/fetch_utils.js";

export function activate_popup(event, popup, overlay, focus_element) {

    event.preventDefault();
    
    popup.style.display = "block";
    overlay.style.display = "block";
    
    focus_element.focus();
}


export function deactivate_popup(event, popup, overlay) {

    event.preventDefault();

    popup.style.display = "none";
    overlay.style.display = "none";
    reset_inputs(popup);
}


export function reset_inputs(popup) {

    let inputs = popup.querySelectorAll('input');

    for (let input of inputs) {
        input.value = "";
        input.removeAttribute("style");
    }
}


export async function add_new_client(event, inputs, popup_side_msg) {

    event.preventDefault();

    let ans = await make_request(inputs);

    if (Object.keys(ans).length > 0) {

        for (let key in ans) {

            let input = document.querySelector(`#${key}`);
            input.style.border = "1px solid red";
        }

        popup_side_msg.classList.remove("sucessful-registration");
        popup_side_msg.classList.add("failed-registration");
        popup_side_msg.innerHTML = "Há campos com valores inválidos!";

    } else {

        for (let input of inputs) {
            input.value = "";
            input.style.border = "1px solid rgb(58, 152, 64)";
        }

        popup_side_msg.classList.remove("failed-registration");
        popup_side_msg.classList.add("sucessful-registration");
        popup_side_msg.innerHTML = "Registro feito com sucesso!";
    }
    
}
