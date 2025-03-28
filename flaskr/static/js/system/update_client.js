"use strict"

import { make_request } from "../utils/fetch_utils.js";


const search_popup = document.querySelector('.search-client-popup');
const popup_side_msg = search_popup.querySelector('.popup-side-msg');
const search_form = search_popup.querySelector('form');
const edit_bt = search_popup.querySelector('.edit-bt');
const visit_bt = search_popup.querySelector('.visit-bt');


export async function update_client(form, pressed_bt, side_msg=null) {

    let inputs = [...form.querySelectorAll("input")];
    inputs.push(pressed_bt);

    let ans = await make_request(inputs, form.action);

    if (ans.status == 400) {

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Número de telefone inválido!";
        }

    } else if (ans.status == 404) {

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Cliente não encontrado!";
        }

    } else if (ans.status == 200) {

        alert("Informações atualizadas com sucesso!");
        window.location.reload();

    } else if (ans.status == 201) {

        alert("Visita registrada com sucesso!");
        window.location.reload();

    }

}


export function init_listeners() {

    edit_bt.addEventListener("click", (event) => {
        event.preventDefault();
        update_client(search_form, edit_bt, popup_side_msg);
    })

    visit_bt.addEventListener("click", (event) => {
        event.preventDefault();
        update_client(search_form, visit_bt, popup_side_msg);
    })

}

init_listeners();