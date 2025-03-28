"use strict"

import { make_request } from "../utils/fetch_utils.js";
import { activate_popup, deactivate_popup, reset_inputs } from "../utils/popup_utils.js";
import { format_birth_date, format_cpf, format_phone_number } from "../utils/formatters.js";


const activate_add_popup_bt = document.querySelector('.activate-add-popup-bt');

const overlay = document.querySelector('.overlay');
const new_client_popup = document.querySelector('.new-client-popup');
const close_popup_bt = new_client_popup.querySelector('.close-popup-bt');
const new_client_form = new_client_popup.querySelector('form');
const popup_side_msg = new_client_popup.querySelector('.popup-side-msg');
const confirm_client_bt = new_client_form.querySelector('.confirm-bt');

const name_input = new_client_popup.querySelector("input[name='name']");
const cpf_input = new_client_popup.querySelector("input[name='cpf']");
const phone_number_input = new_client_popup.querySelector("input[name='phone-number']");
const birth_date_input = new_client_popup.querySelector("input[name='birth-date']");

export async function add_client(form, side_msg=null) {

    let inputs = form.querySelectorAll("input");
    let ans = await make_request(inputs, form.action);
    
    for (let input of inputs) {
        input.removeAttribute("style");
    }

    if (ans.status == 400) {

        let ans_json = await ans.json();

        for (let input_name of ans_json.errors) {
        
            let input = form.querySelector(`input[name='${input_name}']`);
            input.style.border = "1px solid red";
        }

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Há campos com valores inválidos!";
        }


    } else if (ans.status == 409) {

        for (let input of inputs) {
            input.style.border = "1px solid red";
        }


        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Cliente já existe!";
        }


    } else if (ans.status == 201) {
        window.location.reload();
    }
    
}


export function init_listeners() {

    activate_add_popup_bt.addEventListener("click", (event) => {
        event.preventDefault();
        activate_popup(new_client_popup, overlay, name_input);
    })

    close_popup_bt.addEventListener("click", (event) => {
        event.preventDefault();
        deactivate_popup(new_client_popup, overlay, true);
    })

    overlay.addEventListener("click", () => {
        deactivate_popup(new_client_popup, overlay, true);
    })

    cpf_input.addEventListener("input", (event) => {
        format_cpf(event.target);
    })

    phone_number_input.addEventListener("input", (event) => {
        format_phone_number(event.target);
    })

    birth_date_input.addEventListener("input", (event) => {
        format_birth_date(event.target);
    })

    confirm_client_bt.addEventListener("click", (event) => {
        event.preventDefault();
        add_client(new_client_form, popup_side_msg);
    })

    new_client_popup.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            add_client(new_client_form, popup_side_msg);
        }
    })

    addEventListener("DOMContentLoaded", () => {
        reset_inputs(new_client_form);
    })

}

init_listeners();