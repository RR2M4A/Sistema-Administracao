'use strict'

const edit_bts = [...document.querySelectorAll('.edit-bt')];
const delete_bts = [...document.querySelectorAll('.delete-bt')];
const popup = document.querySelector('.popup');
const overlay = document.querySelector('.overlay');
const popup_username = document.querySelector('.popup__username');
const radio_admin_false = document.querySelector('input[name="is-admin"][value="false"]');
const radio_blocked_false = document.querySelector('input[name="is-blocked"][value="false"]');

async function fetch_info(id) {

    let response = await fetch(window.location.href, {
        method: "POST",
        body: JSON.stringify({id: id}),
        headers: {"content-type": "application/json"}
    });

    let data = await response.json();
    return data;
}

async function load_popup(user_info) {

    user_info = await user_info;
    console.log(user_info)

    popup.style.display = "block";
    overlay.style.display = "block";
    popup_username.value = user_info.username;

    if (!user_info.is_admin) {
        radio_admin_false.checked = true;
    }

    if (!user_info.is_blocked) {
        radio_blocked_false.checked = true;
    }
} 

function init_listeners() {

    edit_bts.map((bt) => {
        bt.addEventListener("click", () => {

            let user = bt.parentNode;
            let id = user.id;
            let user_info = fetch_info(id);

            load_popup(user_info);
            
        })
    })
}


init_listeners();