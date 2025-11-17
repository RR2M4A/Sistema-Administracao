"use strict"


import { post } from '../lib/api.js';


const elements = {
    form: document.querySelector('#signin-form'),
    submitBt: document.querySelector('.submit-bt'),
    usernameInput: document.querySelector('input[name="username"]'),
    allInputs: document.querySelectorAll('form input'),
    sideMsg: document.querySelector('.invalid-credentials')
};


const api = {
    async signin(form, inputsNodeList) {
        const route = form.getAttribute('action');
        const payload = {};

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

    clearInputsAndFocus() {
        elements.allInputs.forEach((input) => {
            input.value = "";
        });
        if (elements.usernameInput) {
            elements.usernameInput.focus();
        }
    },

    redirectTo(url) {
        window.location.href = url;
    }
};


const handlers = {
    async handleSignin(event) {
        event.preventDefault();

        try {
            const data = await api.signin(elements.form, elements.allInputs);
            ui.redirectTo(data.redirect);

        } catch (error) {
            ui.showError(error.message);
            ui.clearInputsAndFocus();
        }
    }
};


export function initSignin() {
    if (!elements.form) return;

    elements.submitBt.addEventListener("click", handlers.handleSignin);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            handlers.handleSignin(event);
        }
    });

    addEventListener("DOMContentLoaded", () => {
        ui.clearInputsAndFocus();
    });
}