"use strict"

import * as api from '../lib/api.js';
import * as ui from '../lib/ui.js';

import { activate_popup, deactivate_popup } from '../lib/popup_utils.js';

const elements = {
    overlay: document.querySelector('.overlay'),
    popup: document.querySelector('.new-user-popup'),
    popupForm: document.querySelector(".new-user-popup .popup__form"),
    newUserBt: document.querySelector('.new-user-bt'),
    usernameInput: document.querySelector('.new-user-popup .popup__username'),
    sideMsg: document.querySelector('.side-msg'),
    submitBt: document.querySelector('.new-user-popup__submit'),
    allInputs: document.querySelectorAll('.new-user-popup input')
};

const uiLogic = {
    showPopup() {
        if (elements.popupForm) {
            elements.popupForm.setAttribute("action", "/admin/new/");
        }
        ui.clearFeedback(elements.sideMsg);
        activate_popup(elements.popup, elements.overlay, elements.usernameInput);
    },

    hidePopup() {
        if (!elements.popup || elements.popup.style.display === 'none') return;

        deactivate_popup(elements.popup, elements.overlay, true);
        ui.clearFeedback(elements.sideMsg);
    }
};

const handlers = {
    async handleSubmit(event) {
        event.preventDefault();
        ui.clearFeedback(elements.sideMsg);
        const payload = {};
        for (let input of elements.allInputs) {
            payload[input.name] = input.value;
        }

        try {
            const data = await api.adminCreateNewUser(payload);
            ui.showFeedback(elements.sideMsg, data.msg || "Usuário criado com sucesso!", false);

            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } catch (error) {
            ui.showFeedback(elements.sideMsg, error.message, true);
        }
    }
};

export function initNewUser() {
    if (elements.newUserBt) {
        elements.newUserBt.addEventListener("click", uiLogic.showPopup);
    }
    if (elements.submitBt) {
        elements.submitBt.addEventListener("click", handlers.handleSubmit);
    }
    if (elements.overlay) {
        elements.overlay.addEventListener("click", uiLogic.hidePopup);
    }
}