"use strict"

import { make_request } from "../utils/fetch_utils.js";

const submit_bt = document.querySelector('.submit-bt');
const username_input = document.querySelector('input[name="username"]');
const pass_inputs = document.querySelectorAll('input[type="password"]');
const inputs = document.querySelectorAll('form input');
const side_msg = document.querySelector('.invalid-credentials');


export async function signup(inputs, side_msg) {

    let ans = await make_request(inputs);
    
    if (ans.status == 400) {

        side_msg.style.display = "block";
        side_msg.innerHTML = "Seu nome de usuário não segue o padrão válido!";

    } else if (ans.status == 401) {

        side_msg.style.display = "block";
        side_msg.innerHTML = "As senhas não conferem!";

        pass_inputs[0].focus();
        pass_inputs.forEach((input) => {
            input.value = "";
        })

    } else if (ans.status == 201) {

        alert("Usuário criado com sucesso!");
        window.location.reload();
    }

}


export function init_listeners() {

    submit_bt.addEventListener("click", (event) => {
        event.preventDefault();
        signup(inputs, side_msg)
    });

    document.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            event.preventDefault();
            signup(inputs, side_msg);
        }
    })

    addEventListener("DOMContentLoaded", () => {
        username_input.focus();

        inputs.forEach((input) => {
            input.value = "";
        })
    })
}


init_listeners();