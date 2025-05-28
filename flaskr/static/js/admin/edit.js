'use strict'

const edit_bts = [...document.querySelectorAll('.edit-bt')];
const delete_bts = [...document.querySelectorAll('.delete-bt')];
const popup = document.querySelector('.popup');
const overlay = document.querySelector('.overlay');
const popup_username = document.querySelector('.popup__username');
const radio_admin_false = document.querySelector('input[name="is-admin"][value="false"]');
const radio_blocked_false = document.querySelector('input[name="is-blocked"][value="false"]');
const submit_bt = document.querySelector('.popup__submit');
const hidden_id = document.querySelector('.hidden-id');


let current_user_info = null;


async function fetch_info(id) {
    const response = await fetch(window.location.href, {
        method: "POST",
        body: JSON.stringify({id}),
        headers: { "content-type": "application/json" }
    });

    const data = await response.json();
    return data;
}

async function load_popup(id) {

    current_user_info = (await fetch_info(id)).user;

    popup.style.display = "block";
    overlay.style.display = "block";
    popup_username.value = current_user_info.username;
    hidden_id.value = id;

    if (!current_user_info.is_admin) {
        radio_admin_false.checked = true;
    }

    if (!current_user_info.is_blocked) {
        radio_blocked_false.checked = true;
    }
}


function unload_popup() {
    popup.style.display = 'none';
    overlay.style.display = 'none';
}

function init_listeners() {
    edit_bts.forEach((bt) => {
        bt.addEventListener("click", () => {

            let user = bt.parentNode;
            let id = user.id;
            load_popup(id);

        });
    });

    overlay.addEventListener("click", unload_popup);
}

init_listeners();
