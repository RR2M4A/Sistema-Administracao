// static/js/modules/searchClient.js
"use strict";

import * as api from '../lib/api.js';
import * as ui from '../lib/ui.js';
import { formatCpf } from '../lib/formatters.js';

const elements = {
    form: document.querySelector('.search-form'),
    searchBt: document.querySelector('.search-client-bt'),
    searchBar: document.querySelector('.search-bar'),
    searchMsg: document.querySelector('.search-msg'),
    radioButtons: document.querySelectorAll('.search-form input[type="radio"]'),
    tableBody: document.querySelector(".client-table-body")
};

const handlers = {
    async handleSearch(event) {
        event.preventDefault();
        ui.clearFeedback(elements.searchMsg);

        const markedRadio = document.querySelector("input[name='search']:checked");
        const searchBy = markedRadio.value;
        const value = elements.searchBar.value;

        try {
            const data = await api.getClientEntrances(searchBy, value);
            ui.updateTable(elements.tableBody, data.results);
        } catch (error) {
            if (error.status === 400) {
                ui.showFeedback(elements.searchMsg, "Valor inválido!", true);
            } else if (error.status === 404) {
                ui.showFeedback(elements.searchMsg, "Cliente não encontrado!", true);
            } else {
                ui.showFeedback(elements.searchMsg, error.message, true);
            }
        }
    },

    handleRadioChange() {
        elements.searchBar.value = "";
        ui.clearFeedback(elements.searchMsg);
    },

    handleSearchbarInput() {
        const markedRadio = document.querySelector("input[name='search']:checked");
        if (markedRadio.value === "cpf") {
            formatCpf(elements.searchBar);
        }
    }
};

export function initSearchClient() {
    if (!elements.form) return;

    elements.searchBt.addEventListener("click", handlers.handleSearch);
    elements.searchBar.addEventListener("keydown", (event) => {
        if (event.key === "Enter") handlers.handleSearch(event);
    });

    elements.searchBar.addEventListener("input", handlers.handleSearchbarInput);
    elements.radioButtons.forEach(radio => {
        radio.addEventListener("change", handlers.handleRadioChange);
    });
}