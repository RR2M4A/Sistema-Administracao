// static/js/admin/delete.js
'use strict'

import * as api from '../lib/api.js';

const elements = {
    deleteBts: document.querySelectorAll('.delete-bt')
};


const handlers = {
    async handleDeleteClick(event) {
        const button = event.currentTarget;

        const user = button.parentNode;
        const id = user.id;
        const username = button.previousElementSibling.previousElementSibling.innerHTML;

        if (confirm(`Tem certeza que deseja remover "${username}?"`)) {

            try {
                const data = await api.adminDeleteUser(id);

                alert(data.msg);
                window.location.reload();

            } catch (error) {
                alert(error.message);
            }
        }
    }
};

export function initDeleteUsers() {
    if (elements.deleteBts.length > 0) {
        elements.deleteBts.forEach(bt => {
            bt.addEventListener("click", handlers.handleDeleteClick);
        });
    }
}