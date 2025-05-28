'use strict'

import { fetchInfo } from "../utils/fetch_utils.js";

const overlay = document.querySelector('.overlay');
const popup = document.querySelector('.new-user-popup');
const popupForm = document.querySelector(".new-user-popup .popup__form");
const newUserBt = document.querySelector('.new-user-bt');
const usernameInput = document.querySelector('.new-user-popup .popup__username');
const sideMsg = document.querySelector('.side-msg');
const submitBt = document.querySelector('.new-user-popup__submit');
const inputs = [...document.querySelectorAll('.new-user-popup input')];


async function loadPopup() {
    popup.style.display = "block";
    overlay.style.display = "block";
    popupForm.setAttribute("action", "/admin/new/");
    usernameInput.focus();
}

function unloadPopup() {
    popup.style.display = 'none';
    overlay.style.display = 'none';
    popupForm.reset();
    sideMsg.innerHTML = "";
}

export async function signup() {

    let entry = {}

    for (let input of inputs) {
        entry[input.name] = input.value;
    }

    let url = `${window.location.origin}/admin/new/`
    let ans = await fetchInfo(url, entry);

    if (ans.status == 201) {
        alert("Usuário criado com sucesso!")
        window.location.reload();
    }

    let data = await ans.json();
    sideMsg.innerHTML = data.msg;
}

function init_listeners() {
    newUserBt.addEventListener("click", evt => {
        loadPopup();
    })

    submitBt.addEventListener("click", evt => {
        evt.preventDefault();
        signup();

    })

    overlay.addEventListener("click", unloadPopup);
}

init_listeners();
