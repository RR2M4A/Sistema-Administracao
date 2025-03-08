"use strict"

import * as pp from "./popup.js";

const add_client_bt = document.querySelector('.add-client-bt');
const popup = document.querySelector('.popup');
const overlay = document.querySelector('.overlay');
const close_popup_bt = document.querySelector('.close-popup-bt');
const confirm_client_bt = document.querySelector('.confirm-bt');
const name_input = document.querySelector('#name');
const rg_input = document.querySelector('#rg');
const cpf_input = document.querySelector('#cpf');
const phone_number_input = document.querySelector('#phone-number');
const birth_date_input = document.querySelector('#birth-date');

add_client_bt.addEventListener("click", (event) => {pp.activate_popup(event, popup, overlay, name_input)});
overlay.addEventListener("click", (event) => {pp.deactivate_popup(event, popup, overlay)});
close_popup_bt.addEventListener("click", (event) => {pp.deactivate_popup(event, popup, overlay)});

cpf_input.addEventListener("input", pp.format_cpf);
phone_number_input.addEventListener("input", pp.format_phone_number);
birth_date_input.addEventListener("input", pp.format_birth_date);

confirm_client_bt.addEventListener("click", add_new_client);