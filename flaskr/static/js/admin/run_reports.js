'use strict';

import * as api from '../lib/api.js';
import * as ui from '../lib/ui.js';
import { formatBirthDate } from '../lib/formatters.js';
import { activate_popup, deactivate_popup } from '../lib/popup_utils.js';

const elements = {
    overlay: document.querySelector('.overlay'),
    reportBt: document.querySelector('.run-report-bt'),
    generateReportsBt: document.querySelector('.generate-report-bt'),
    reportBox: document.querySelector('.report-box'),
    reportForm: document.querySelector('.report-box form'),
    startDateInput: document.querySelector('.start-date'),
    finalDateInput: document.querySelector('.final-date'),
    sideMsg: document.querySelector('.report-box__side-msg')
};

const uiLogic = {
    showReportBox() {
        ui.clearFeedback(elements.sideMsg);
        activate_popup(elements.reportBox, elements.overlay, elements.startDateInput);
    },

    hideReportBox() {
        if (!elements.reportBox || elements.reportBox.style.display === 'none') return;
        deactivate_popup(elements.reportBox, elements.overlay, false);
        ui.clearFeedback(elements.sideMsg);
    }
};

const handlers = {
    async handleSubmitReport(event) {
        event.preventDefault();
        ui.clearFeedback(elements.sideMsg);

        const payload = {
            "start-date": elements.startDateInput.value,
            "final-date": elements.finalDateInput.value
        };

        try {
            const blob = await api.adminRunReport(payload);
            ui.downloadFile(blob, "relatorio.xlsx");
            uiLogic.hideReportBox();

        } catch (error) {
            ui.showFeedback(elements.sideMsg, error.message, true);
        }
    }
};

export function initRunReports() {
    if (elements.generateReportsBt) {
        elements.generateReportsBt.addEventListener("click", handlers.handleSubmitReport);
    }
    if (elements.reportBt) {
        elements.reportBt.addEventListener("click", uiLogic.showReportBox);
    }
    if (elements.overlay) {
        elements.overlay.addEventListener("click", uiLogic.hideReportBox);
    }

    if (elements.startDateInput) {
        elements.startDateInput.addEventListener("input", (e) => formatBirthDate(e.target));
    }
    if (elements.finalDateInput) {
        elements.finalDateInput.addEventListener("input", (e) => formatBirthDate(e.target));
    }
}