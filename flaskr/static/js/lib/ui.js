"use strict";

export function enableInput(input) {
    if (!input) return;
    input.disabled = false;
    input.removeAttribute("style");
}

export function disableInput(input) {
    if (!input) return;
    input.disabled = true;
    input.style.background = "#9c9c9c"; // ou #e1e1e1, etc.
}

export function updateTable(tbody, results) {
    if (!tbody) return;
    tbody.innerHTML = ""; // Limpa a tabela
    for (let c of results) {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${c.name}</td>
            <td>${c.cpf}</td>
            <td>${c.phone_number}</td>
            <td>${c.birth_date}</td>
            <td>${c.department}</td>
            <td>${c.date}</td>
            <td>${c.time}</td>
        `;
        tbody.appendChild(row);
    }
}

export function showFeedback(element, message, isError = true) {
    if (!element) return;
    element.innerHTML = message;
    element.classList.toggle("failed-msg", isError);
    element.classList.toggle("successful-msg", !isError);
}

export function clearFeedback(element) {
    if (!element) return;
    element.innerHTML = "";
    element.classList.remove("failed-msg", "successful-msg");
}

export function showValidationErrors(form, errorFields) {
    if (!form) return;
    // Limpa erros antigos
    form.querySelectorAll("input, select").forEach(input => input.removeAttribute("style"));

    // Aplica novos erros
    for (const input_name of errorFields) {
        const input = form.querySelector(`input[name='${input_name}']`) ||
                      form.querySelector(`select[name='${input_name}']`);
        if (input) {
            input.style.border = "1px solid red";
        }
    }
}

export function clearValidationErrors(form) {
    if (!form) return;
    form.querySelectorAll("input, select").forEach(input => input.removeAttribute("style"));
}

export function loadClientInfo(inputs, clientInfo) {
    if (inputs.name) inputs.name.value = clientInfo.name;
    if (inputs.rg) inputs.rg.value = clientInfo.rg;
    if (inputs.cpf) inputs.cpf.value = clientInfo.cpf;
    if (inputs.phoneNumber) inputs.phoneNumber.value = clientInfo.phone_number;
    if (inputs.birthDate) inputs.birthDate.value = clientInfo.birth_date;
}