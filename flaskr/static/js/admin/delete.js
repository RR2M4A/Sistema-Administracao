'use strict'

import { fetchInfo } from "../utils/fetch_utils.js";


const deleteBts = document.querySelectorAll('.delete-bt')


async function delete_user(id, username) {

    if (confirm(`Tem certeza que deseja remover "${username}?"`)) {

        let url = `${window.location.origin}/admin/delete/`;
        let ans = await fetchInfo(url, {id: id});
        let data = await ans.json();

        alert(data['msg'])
        window.location.reload();
    }

}


function init_listeners() {
    deleteBts.forEach(bt => {
        bt.addEventListener("click", () => {
            let user = bt.parentNode;
            let username = bt.previousElementSibling.previousElementSibling.innerHTML;
            let id = user.id;

            delete_user(id, username);
        });
    });
}

init_listeners();

