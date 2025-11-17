'use strict'

import * as api from '../lib/api.js';
import * as ui from '../lib/ui.js';
import { activate_popup, deactivate_popup } from '../lib/popup_utils.js';

const elements = {
    editBts: document.querySelectorAll('.edit-bt'),
    popup: document.querySelector('.popup'),
    overlay: document.querySelector('.overlay'),
    popupUsername: document.querySelector('.popup .popup__username'),
    hiddenId: document.querySelector('.hidden-id'),
    popupForm: document.querySelector(".popup .popup__form"),
    sideMsg: document.querySelector('.popup .popup-side-msg'),
    submitBt: document.querySelector('.popup__submit')
};

const uiLogic = {
    showPopup(userInfo) {
        ui.clearFeedback(elements.sideMsg);

        if (elements.popupUsername) {
            elements.popupUsername.value = userInfo.username;
            elements.popupUsername.disabled = true;
        }
        if (elements.hiddenId) {
            elements.hiddenId.value = userInfo.id;
        }

        const adminRadio = document.querySelector(`input[name="is-admin"][value="${userInfo.is_admin}"]`);
        if (adminRadio) adminRadio.checked = true;

        const activeRadio = document.querySelector(`input[name="is-active"][value="${userInfo.is_active}"]`);
        if (activeRadio) activeRadio.checked = true;

        activate_popup(elements.popup, elements.overlay, null);
    },

    hidePopup() {
        if (!elements.popup || elements.popup.style.display === 'none') return;
        deactivate_popup(elements.popup, elements.overlay, true);
        if (elements.popupForm) elements.popupForm.reset();
        ui.clearFeedback(elements.sideMsg);
    }
};

const handlers = {
    async handleOpenPopup(event) {
        const button = event.currentTarget;
        const id = button.parentNode.id;

        try {
            const data = await api.adminGetUserInfo(id);
            uiLogic.showPopup(data.user);
        } catch (error) {
            ui.showFeedback(elements.sideMsg, error.message, true);
        }
    },

    async handleSubmit(event) {
        event.preventDefault();
        ui.clearFeedback(elements.sideMsg);

        const formData = new FormData(elements.popupForm);
        const payload = Object.fromEntries(formData.entries());

        payload.username = elements.popupUsername.value;

        try {
            const data = await api.adminUpdateUser(payload);

            ui.showFeedback(elements.sideMsg, data.msg, false);

            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } catch (error) {
            ui.showFeedback(elements.sideMsg, error.message, true);
        }
    }
};

export function initEditUsers() {
    if (elements.editBts.length > 0) {
        elements.editBts.forEach((bt) => {
            bt.addEventListener("click", handlers.handleOpenPopup);
        });
    }

    if (elements.overlay) {
        elements.overlay.addEventListener("click", uiLogic.hidePopup);
    }

    if (elements.submitBt) {
        elements.submitBt.addEventListener("click", handlers.handleSubmit);
    }
}