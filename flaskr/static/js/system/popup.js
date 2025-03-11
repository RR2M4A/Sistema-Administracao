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


export function format_cpf(event) {

    event.preventDefault();

    let input = event.target;
    let start = input.selectionStart;
    let old_value = input.value;

    let value = input.value.replace(/\D/g, "");

    if (value.length > 3) {
        value = value.slice(0, 3) + "." + value.slice(3);
    }

    if (value.length > 7) {
        value = value.slice(0, 7) + "." + value.slice(7);
    }

    if (value.length > 11) {
        value = value.slice(0, 11) + "-" + value.slice(11);
    }

    if (value.length > 14) {
        value = value.slice(0, 14);
    }

    input.value = value;
    
    let diff = input.value.length - old_value.length;
    input.setSelectionRange(start + diff, start + diff);

}


export function format_phone_number(event) {

    event.preventDefault();

    let input = event.target;
    let start = input.selectionStart;
    let old_value = input.value;

    let value = input.value.replace(/\D/g, "");

    if (value.length > 0) {
        value = "(" + value;
    }

    if (value.length > 3) {
        value = value.slice(0, 3) + ") " + value.slice(3);
    }

    if (value.length > 9) {
        value = value.slice(0, 9) + "-" + value.slice(9);
    }

    if (value.length > 14) {
        value = value.replace("-", "");
        value = value.slice(0, 10) + "-" + value.slice(10, 14);
    }

    if (value.length > 15) {
        value = value.slice(0, 15);
    }

    input.value = value;

    let diff = input.value.length - old_value.length;
    input.setSelectionRange(start + diff, start + diff);

}


export function format_birth_date(event) {
    
    event.preventDefault();

    let input = event.target;
    let start = input.selectionStart;
    let old_value = input.value;

    let value = input.value.replace(/\D/g, "");

    if (value.length > 2) {
        value = value.slice(0, 2) + "/" + value.slice(2);
    }

    if (value.length > 5) {
        value = value.slice(0, 5) + "/" + value.slice(5);
    }

    if (value.length > 10) {
        value = value.slice(0, 10);
    }

    input.value = value;

    let diff = input.value.length - old_value.length;
    input.setSelectionRange(start + diff, start + diff);
}


export async function add_new_client(event, inputs, popup_side_msg) {

    event.preventDefault();

    let ans = await make_request(inputs);
    let all_valid = true;

    for (let obj of ans) {
        
        let input = document.querySelector(`#${obj.input}`);

        if (!obj.is_valid) {
            input.style.border = "1px solid red";
            all_valid = false

        } else {
            input.style.border = "1px solid rgb(58, 152, 64)";
        }
    }

    if (all_valid) {
        popup_side_msg.classList.remove("failed-registration");
        popup_side_msg.classList.add("sucessful-registration");
        popup_side_msg.innerHTML = "Registro feito com sucesso!";

    } else {
        popup_side_msg.classList.remove("sucessful-registration");
        popup_side_msg.classList.add("failed-registration");
        popup_side_msg.innerHTML = "Há campos com valores inválidos!";
    }
    
}
