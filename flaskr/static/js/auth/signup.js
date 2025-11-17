"use strict"


import { post } from '../lib/api.js';


const elements = {
    form: document.querySelector('#signup-form'),
    submitBt: document.querySelector('.submit-bt'),
    usernameInput: document.querySelector('input[name="username"]'),
    passInputs: document.querySelectorAll('input[type="password"]'),
    allInputs: document.querySelectorAll('form input'),
    sideMsg: document.querySelector('.invalid-credentials')
};


const api = {
    async signup(form, inputsNodeList) {
        const route = form.getAttribute('action');
        const payload = {}

        for (let input of inputsNodeList) {
            payload[input.name] = input.value;
        }

        return post(route, payload);
    }
};


const ui = {
    showError(message) {
        if (elements.sideMsg) {
            elements.sideMsg.style.display = "block";
            elements.sideMsg.innerHTML = message;
        }
    },
    clearPasswordInputs() {
        elements.passInputs.forEach((input) => {
            input.value = "";
        });
        if (elements.passInputs[0]) {
            elements.passInputs[0].focus();
        }
    },
    clearAllInputs() {
        elements.allInputs.forEach((input) => {
            input.value = "";
        });
    },
    focusUsername() {
        if (elements.usernameInput) {
            elements.usernameInput.focus();
        }
    },
    showAlertAndReload(message) {
        alert(message);
        window.location.reload();
    }
};


const handlers = {
    async handleSignup(event) {
        event.preventDefault();

        try {
            const data = await api.signup(elements.form, elements.allInputs);
            ui.showAlertAndReload(data.msg);

        } catch (error) {
            ui.showError(error.message);

            if (error.status === 401) {
                ui.clearPasswordInputs();
            }
        }
    }
};


export function initSignup() {
    if (!elements.form) return;

    elements.submitBt.addEventListener("click", handlers.handleSignup);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            handlers.handleSignup(event);
        }
    });

    addEventListener("DOMContentLoaded", () => {
        ui.focusUsername();
        ui.clearAllInputs();
    });
}