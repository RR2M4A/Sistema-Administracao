"use strict"

import { validate_credentials } from "./credentials.js";

const submit_bt = document.querySelector('.submit-bt');
const username_input = document.querySelector("#username");
const password_input = document.querySelector("#password");

submit_bt.addEventListener("click", (event) => {validate_credentials(event, username_input, password_input)});

document.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        validate_credentials(event, username_input, password_input);
    }
})