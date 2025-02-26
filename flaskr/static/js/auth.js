"use strict"

const username_input = document.querySelector('#username');
const password_input = document.querySelector('#password');
const submit_bt = document.querySelector('.submit-bt');
const wrong_credentials_msg = document.querySelector('.wrong-credentials');

submit_bt.addEventListener("click", validate_credentials);

async function validate_credentials(event) {

    event.preventDefault();

    let entry = {
        "username": username_input.value,
        "password": password_input.value
    }

    let response = await fetch(window.location.href, {
        method: "POST",
        body: JSON.stringify(entry),
        headers: {"content-type": "application/json"}
    });

    let data = await response.json();
    
    if (data.authenticated == "false") {
        wrong_credentials_msg.style.display = "block";
    } else {
        window.location.href = data.redirect;
    }

}