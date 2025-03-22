"use strict"

import * as pp from "./popup.js";
import * as fm from "../utils/formatters.js";
import { hide_side_msg, search_client } from "./search.js";
import { reload } from "./reload.js";

const search_form = document.querySelector('.search-form');
const search_client_bt = document.querySelector('.search-client-bt');
const search_msg = document.querySelector('.search-msg');
const search_bar = document.querySelector('.search-bar');
const radio_inputs = document.querySelectorAll('.radio-bt');

const add_client_bt = document.querySelector('.add-client-bt');
const popup = document.querySelector('.popup');
const popup_form = document.querySelector('.popup form');
const popup_side_msg = document.querySelector('.popup-side-msg');
const overlay = document.querySelector('.overlay');
const close_popup_bt = document.querySelector('.close-popup-bt');
const confirm_client_bt = document.querySelector('.confirm-bt');

const reload_bt = document.querySelector('.reload-bt');

const name_input = document.querySelector('#name');
const cpf_input = document.querySelector('#cpf');
const phone_number_input = document.querySelector('#phone-number');
const birth_date_input = document.querySelector('#birth-date');

search_client_bt.addEventListener("click", (event) => {search_client(event, search_form, search_msg)});

add_client_bt.addEventListener("click", (event) => {pp.activate_popup(event, popup, overlay, name_input)});
overlay.addEventListener("click", (event) => {pp.deactivate_popup(event, popup, overlay)});
close_popup_bt.addEventListener("click", (event) => {pp.deactivate_popup(event, popup, overlay)});

cpf_input.addEventListener("input", fm.format_cpf);
phone_number_input.addEventListener("input", fm.format_phone_number);
birth_date_input.addEventListener("input", fm.format_birth_date);

confirm_client_bt.addEventListener("click", (event) => {pp.add_new_client(event, popup_form, popup_side_msg)});

popup.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        pp.add_new_client(event, popup_form, popup_side_msg);
    }
})

search_bar.addEventListener("input", (event) => {
    let marked_input = document.querySelector('input[name="search"]:checked');

    if (marked_input.value == "cpf") {
        fm.format_cpf(event);
    }
})

search_bar.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        search_client(event, search_form, search_msg);
    }
});

radio_inputs.forEach((element) => {
    element.addEventListener("change", () => {
        search_bar.value = "";
        hide_side_msg(search_msg);
    })
})

document.addEventListener("DOMContentLoaded", () => {
    pp.reset_inputs(popup_form);
    pp.reset_inputs(search_form);
})

reload_bt.addEventListener("click", reload);