"use strict"

import { make_request } from "../utils/fetch_utils.js";


export function activate_popup(event, popup, overlay, focus_element) {

    event.preventDefault();
    
    popup.style.display = "block";
    overlay.style.display = "block";
    
    focus_element.focus();
}


export function deactivate_popup(event, popup, overlay) {

    event.preventDefault();

    popup.querySelector(".popup-side-msg").innerHTML = "";
    popup.style.display = "none";
    overlay.style.display = "none";
    reset_inputs(popup);
}


export function reset_inputs(parent) {

    let inputs = parent.querySelectorAll('input');

    for (let input of inputs) {
        if (input.type != "radio") {
            input.value = "";
            input.removeAttribute("style");
        }
    }
}


export async function add_new_client(event, form, side_msg=null) {

    event.preventDefault();

    let inputs = form.querySelectorAll("input");
    let ans = await make_request(inputs, form.action);

    if (ans.status == 400) {

        let ans_json = await ans.json();

        for (let input_id of ans_json.errors) {
        
            let input = document.querySelector(`#${input_id}`);
            input.style.border = "1px solid red";
        }

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Há campos com valores inválidos!";
        }


    } else if (ans.status == 409) {

        for (let input of inputs) {
            input.style.border = "1px solid red";
        }


        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Cliente já existe!";
        }


    } else if (ans.status == 201) {

        window.location.reload();

    }
    
}
