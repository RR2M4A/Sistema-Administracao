"use strict"

import { make_request } from "../utils/fetch_utils.js";
import { activate_popup, deactivate_popup} from "../utils/popup_utils.js";
import { format_cpf, format_phone_number} from "../utils/formatters.js";


const search_form = document.querySelector('.search-form');
const search_client_bt = document.querySelector('.search-client-bt');
const search_form_radio_bts = search_form.querySelectorAll('input[type="radio"]');
const search_form_inputs = search_form.querySelectorAll('input');
const search_bar = document.querySelector('.search-bar');
const search_msg = document.querySelector('.search-msg');

const overlay = document.querySelector('.overlay');
const search_popup = document.querySelector(".search-client-popup");
const close_popup_bt = document.querySelector(".close-popup-bt");
const form = search_popup.querySelector("form");

const text_inputs = form.querySelectorAll('input:not([type="radio"])');
const radio_inputs = form.querySelectorAll('input[type="radio"]');
const client_id_input = form.querySelector('.client-id');
const name_input = form.querySelector("input[name='name']");
const rg_input = form.querySelector("input[name='rg']");
const cpf_input = form.querySelector("input[name='cpf']");
const phone_number_input = form.querySelector("input[name='phone-number']");
const birth_date_input = form.querySelector("input[name='birth-date']");

const edit_bt = form.querySelector('.edit-bt');


export async function search_client(form, side_msg=null) {

    let ans = await make_request(search_form_inputs, "/system/search_client");

    if (ans.status == 400) {

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Valor inválido!";
        }
        
    } else if (ans.status == 404) {

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Cliente não encontrado!";    
        }
        
    } else if (ans.status == 200) {

        side_msg.classList.remove("successful-msg");
        side_msg.classList.remove("failed-msg");

        let client_info = await ans.json();

        activate_popup(search_popup, overlay);
        load_popup_info(client_info);

    }

}


export function load_popup_info(client_info) {

    client_id_input.value = client_info.id;
    name_input.value = client_info.name;
    rg_input.value = client_info.rg;
    cpf_input.value = client_info.cpf;
    phone_number_input.value = client_info.phone_number;
    birth_date_input.value = client_info.birth_date;

    for (let input of text_inputs) {
        disable_input(input);
    }

}


export function disable_input(input) {
    input.disabled = true;
    input.style.background = "#e1e1e1";
}


export function enable_input(input) {
    input.disabled = false;
    input.removeAttribute("style");
}


export function init_listeners() {

    search_client_bt.addEventListener("click", (event) => {
        event.preventDefault();
        search_client(form, search_msg);
    })

    search_bar.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            event.preventDefault();
            search_client(form, search_msg);
        }
    })

    close_popup_bt.addEventListener("click", () => {
        deactivate_popup(search_popup, overlay, false);
    })

    search_bar.addEventListener("input", () => {
    
        let marked_radio = document.querySelector("input[name='search']:checked");

        if (marked_radio.value == "cpf") {
            format_cpf(search_bar);
        }
    })

    search_form_radio_bts.forEach((element) => {
        element.addEventListener("change", () => {
            search_bar.value = "";
        })
    })

    radio_inputs.forEach((element) => {
        element.addEventListener("change", (event) => {

            let marked_radio = form.querySelector("input[name='edit']:checked");
            
            if (marked_radio.value == "edit") {
                edit_bt.style.display = "block";
                enable_input(phone_number_input);

            } else {
                edit_bt.removeAttribute("style");

                for (let input of text_inputs) {
                    disable_input(input);
                }
            }
        })
    })

    phone_number_input.addEventListener("input", () => {
        format_phone_number(phone_number_input);
    })

    addEventListener("DOMContentLoaded", () => {
        edit_bt.style.display = "none";
    })

}


init_listeners();