"use strict"

import { make_request } from "../utils/fetch_utils.js";

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