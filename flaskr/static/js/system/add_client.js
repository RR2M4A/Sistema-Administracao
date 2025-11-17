"use strict";

import * as api from '../lib/api.js';
import * as ui from '../lib/ui.js';

import { activate_popup, deactivate_popup, reset_inputs } from '../lib/popup_utils.js';
import { formatBirthDate, formatCpf, formatPhoneNumber } from '../lib/formatters.js';

const elements = {
    activateAddPopupBt: document.querySelector('.activate-add-popup-bt'),
    overlay: document.querySelector('.overlay'),
    popup: document.querySelector('.new-client-popup'),
    closePopupBt: document.querySelector('.new-client-popup .close-popup-bt'),
    form: document.querySelector('#add-client-form'),
    sideMsg: document.querySelector('.new-client-popup .popup-side-msg'),
    confirmBt: document.querySelector('.new-client-popup .confirm-bt'),

    inputs: {
        name: document.querySelector(".new-client-popup input[name='name']"),
        rg: document.querySelector(".new-client-popup input[name='rg']"),
        cpf: document.querySelector(".new-client-popup input[name='cpf']"),
        phoneNumber: document.querySelector(".new-client-popup input[name='phone-number']"),
        birthDate: document.querySelector(".new-client-popup input[name='birth-date']"),
    },

    get keyInputs() {
        return [
            this.inputs.name,
            this.inputs.rg,
            this.inputs.birthDate
        ];
    },

    get allFillableInputs() {
        return [
            this.inputs.name,
            this.inputs.rg,
            this.inputs.phoneNumber,
            this.inputs.birthDate
        ];
    }
};


const handlers = {
    async handleCpfInput(event) {
        formatCpf(event.target);
        const digitsOnly = event.target.value.replace(/\D/g, "");

        if (digitsOnly.length === 11) {
            try {
                ui.clearFeedback(elements.sideMsg);
                const data = await api.getClientInfo(event.target.value);

                ui.loadClientInfo(elements.inputs, data.client_info);
                elements.keyInputs.forEach(ui.disableInput);

                ui.enableInput(elements.inputs.phoneNumber);
                ui.showFeedback(elements.sideMsg, data.msg, false);

            } catch (error) {
                elements.allFillableInputs.forEach(ui.enableInput);
                ui.showFeedback(elements.sideMsg, error.message, false);
            }
        } else {
            const isFormEmpty = elements.allFillableInputs.every(input => input.value === '');
            if (isFormEmpty) {
                elements.allFillableInputs.forEach(ui.disableInput);
                ui.clearFeedback(elements.sideMsg);
            }
        }
    },

    async handleSubmit(event) {
        event.preventDefault();

        if (!elements.form) return;
        ui.clearValidationErrors(elements.form);

        const payload = {}
        const formInputs = elements.form.querySelectorAll("input, select");

        for (let input of formInputs) {
            payload[input.name] = input.value;
        }

        try {
            const data = await api.addClient(payload);
            ui.showFeedback(elements.sideMsg, data.msg, false);

            window.location.reload();

        } catch (error) {
            if (error.status === 400) {
                ui.showValidationErrors(elements.form, error.details.errors);
                ui.showFeedback(elements.sideMsg, "Há campos com valores inválidos!", true);
            } else if (error.status === 409) {
                // ...
            } else {
                ui.showFeedback(elements.sideMsg, error.message, true);
            }
        }
    },

    openPopup(event) {
        event.preventDefault();
        if (elements.form) reset_inputs(elements.form);
        ui.clearFeedback(elements.sideMsg);
        ui.clearValidationErrors(elements.form);

        elements.allFillableInputs.forEach(ui.disableInput);

        activate_popup(elements.popup, elements.overlay, elements.inputs.cpf);
    }
};


export function initAddClient() {
    if (elements.activateAddPopupBt) {
        elements.activateAddPopupBt.addEventListener("click", handlers.openPopup);
    }
    if (elements.closePopupBt) {
        elements.closePopupBt.addEventListener("click", () => deactivate_popup(elements.popup, elements.overlay, true));
    }
    if (elements.overlay) {
        elements.overlay.addEventListener("click", () => deactivate_popup(elements.popup, elements.overlay, true));
    }
    if (elements.inputs.cpf) {
        elements.inputs.cpf.addEventListener("input", handlers.handleCpfInput);
    }
    if (elements.inputs.phoneNumber) {
        elements.inputs.phoneNumber.addEventListener("input", (e) => formatPhoneNumber(e.target));
    }
    if (elements.inputs.birthDate) {
        elements.inputs.birthDate.addEventListener("input", (e) => formatBirthDate(e.target));
    }
    if (elements.confirmBt) {
        elements.confirmBt.addEventListener("click", handlers.handleSubmit);
    }
    if (elements.form) {
        elements.form.addEventListener("keydown", (event) => {
            if (event.key === "Enter") handlers.handleSubmit(event);
        });

        addEventListener("DOMContentLoaded", () => reset_inputs(elements.form));
    }
}