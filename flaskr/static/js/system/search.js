"use strict"

import { make_request } from "../utils/fetch_utils.js";


const tbody = document.querySelector('.table-container tbody');


export async function search_client(event, form, side_msg=null) {

    event.preventDefault();

    let inputs = form.querySelectorAll("input");
    let ans = await make_request(inputs, form.action);

    if (ans.status == 400) {

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Valor inválido!";
        }

    } else if (ans.status == 404) {

        if (side_msg) {
            side_msg.classList.remove("successful-msg");
            side_msg.classList.add("failed-msg");
            side_msg.innerHTML = "Cliente não encontrado!";
        }

    } else if (ans.status == 200) {

        if (side_msg) {
            side_msg.classList.remove("failed-msg");
            side_msg.classList.add("successful-msg");
            side_msg.innerHTML = "Cliente encontrado!";

            setTimeout(() => hide_side_msg(side_msg), 5000);
        }

        let client_info = await ans.json();
        show_client(client_info);
    }
}


export function hide_side_msg(side_msg) {
    side_msg.classList.remove("failed-msg", "successful-msg");
}


export function show_client(client_info) {

    let children = tbody.children;

    if (children.length > 0) {
        for (let child of children) {
            child.style.display = "none";
        }
    }

    let row = document.createElement("tr");
    let properties = ["name", "rg", "cpf", "phone_number", "birth_date"];

    properties.forEach(property => {
        let cell = document.createElement("td");
        cell.innerHTML = client_info[property];
        row.appendChild(cell);
    });

    tbody.appendChild(row);

}