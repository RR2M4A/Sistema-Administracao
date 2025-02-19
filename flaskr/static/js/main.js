"use strict"

const popup = document.querySelector(".popup");
const add_client_bt = document.querySelector('.add-client-bt');
const overlay = document.querySelector('.overlay');
const close_popup_bt = document.querySelector('.close-popup-bt');
const confirm_client_bt = document.querySelector('.confirm-bt');
const name_input = document.querySelector('#name');
const rg_input = document.querySelector('#rg');
const cpf_input = document.querySelector('#cpf');
const phone_number_input = document.querySelector('#phone-number');
const birth_date_input = document.querySelector('#birth-date');

add_client_bt.addEventListener("click", activate_popup);
overlay.addEventListener("click", deactivate_popup);
close_popup_bt.addEventListener("click", deactivate_popup);
confirm_client_bt.addEventListener("click", add_new_client);

function activate_popup(event) {

    event.preventDefault();

    overlay.style.display = "block";
    popup.style.display = "block";
    name_input.focus();
}

function deactivate_popup(event) {

    event.preventDefault();

    overlay.style.display = "none";
    popup.style.display = "none";
}

function add_new_client(event) {
    
    event.preventDefault();

    let entry = {
        "name": name_input.value,
        "rg": rg_input.value,
        "cpf": cpf_input.value,
        "phone_number": phone_number_input.value,
        "birth_date": birth_date_input.value
    }

    console.log("Passou aqui");

    fetch(window.location.href, {
        method: "POST",
        body: JSON.stringify(entry),
        headers: {"content-type": "application/json"}
    })

    .then((response) => {
        return response.json();
    })

    .then((converted_response) => {
        console.log(converted_response);
    })
}