"use strict"

import { make_request } from "../utils/fetch_utils.js";

const submit_bt = document.querySelector('.submit-bt');
const username_input = document.querySelector('input[name="username"]');
const inputs = document.querySelectorAll('form input');
const side_msg = document.querySelector('.invalid-credentials');


export async function validate_credentials(event, inputs, side_msg) {

    event.preventDefault();
    let ans = await make_request(inputs);
    let data = await ans.json();

    if (!data.authenticated) {

        switch (data.status) {
            case "check_credentials":
                side_msg.style.display = "block";
                side_msg.innerHTML = "Credenciais inválidas!"
                break;
            case "blocked":
                side_msg.style.display = "block";
                side_msg.innerHTML = "Conta bloqueada!"
                break
        }

        inputs.forEach((input) => {
            input.value = "";
        })

        username_input.focus();
        return;

    }

    window.location.href = data.redirect;

}


export function init_listeners() {

    submit_bt.addEventListener("click", (event) => {validate_credentials(event, inputs, side_msg)});

    document.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            validate_credentials(event, inputs, side_msg);
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