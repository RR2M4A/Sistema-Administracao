"use strict"

import { make_request } from "../utils/fetch_utils.js";

const submit_bt = document.querySelector('.submit-bt');
const username_input = document.querySelector('input[name="username"]');
const inputs = document.querySelectorAll('form input');
const side_msg = document.querySelector('.wrong-credentials');


export async function validate_credentials(event, inputs, side_msg) {

    event.preventDefault();
    let ans = await make_request(inputs);
    let data = await ans.json();
    
    if (!data.authenticated) {
        side_msg.style.display = "block";
    } else {
        window.location.href = data.redirect;
    }

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