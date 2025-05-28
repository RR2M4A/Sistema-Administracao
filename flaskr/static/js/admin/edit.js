'use strict'

import { fetchInfo } from "../utils/fetch_utils.js";

const editBts = [...document.querySelectorAll('.edit-bt')];
const popup = document.querySelector('.popup');
const overlay = document.querySelector('.overlay');
const popupUsername = document.querySelector('.popup .popup__username');
const hiddenId = document.querySelector('.hidden-id');
const popupForm = document.querySelector(".popup .popup__form");


let currUserInfo = null;


async function loadPopup(id) {

    let entry = {
        id: id
    }

    let ans = await fetchInfo(null, entry);
    currUserInfo = (await ans.json()).user;

    popup.style.display = "block";
    overlay.style.display = "block";
    popupForm.setAttribute("action", "/admin/edit/")

    popupUsername.value = currUserInfo.username;
    popupUsername.disabled = true;
    hiddenId.value = id;

    document.querySelector(`input[name="is-admin"][value="${currUserInfo.is_admin}"]`).checked = true;
    document.querySelector(`input[name="is-active"][value="${currUserInfo.is_active}"]`).checked = true;
}

function unloadPopup() {
    popup.style.display = 'none';
    overlay.style.display = 'none';
    popupForm.reset();
}

function init_listeners() {
    editBts.forEach((bt) => {
        bt.addEventListener("click", () => {
            let user = bt.parentNode;
            let id = user.id;
            loadPopup(id);
        });
    });

    overlay.addEventListener("click", unloadPopup);
}

init_listeners();
