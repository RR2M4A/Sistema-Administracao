"use strict"

import { validate_credentials } from "./credentials.js";

const submit_bt = document.querySelector('.submit-bt');
const inputs = document.querySelectorAll('form input');

submit_bt.addEventListener("click", (event) => {validate_credentials(event, inputs)});

document.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        validate_credentials(event, inputs);
    }
})