"use strict"

export async function validate_credentials(event, username_input, password_input) {

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