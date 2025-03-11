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
    reset_inputs();
}


export function reset_inputs(popup) {

    popup.querySelectorAll('input').forEach(input => input.value = "");
}


export function format_cpf(event) {

    event.preventDefault();

    let input = event.target;
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

}


export function format_phone_number(event) {

    event.preventDefault();

    let input = event.target;
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

}


export function format_birth_date(event) {
    
    event.preventDefault();

    let input = event.target;
    let value = input.value.replace(/\D/g, "");

    if (value.length > 2) {
        value = value.slice(0, 2) + "/" + value.slice(2);
    }

    if (value.length > 7) {
        value = value.slice(0, 7) + "/" + value.slice(7);
    }

    if (value.length > 14) {
        value = value.slice(0, 14);
    }

    input.value = value;
}


export async function add_new_client(event, inputs) {

    event.preventDefault();

    data = await make_request(inputs);

    

}
