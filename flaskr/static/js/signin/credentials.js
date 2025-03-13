"use strict"

import { make_request } from "../utils/fetch_utils.js";

export async function validate_credentials(event, inputs) {

    event.preventDefault();
    let data = await make_request(inputs);
    
    if (!data.authenticated) {
        wrong_credentials_msg.style.display = "block";
    } else {
        window.location.href = data.redirect;
    }

}