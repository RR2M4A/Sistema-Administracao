"use strict"

import { validate_credentials } from "./credentials.js";

const submit_bt = document.querySelector('.submit-bt');
const inputs = document.querySelectorAll('form input');
const side_msg = document.querySelector('.wrong-credentials');

submit_bt.addEventListener("click", (event) => {validate_credentials(event, inputs, side_msg)});

document.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        validate_credentials(event, inputs, side_msg);
    }
})