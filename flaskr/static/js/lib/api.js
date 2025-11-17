// static/js/lib/api.js
"use strict";

/**
 * Faz uma requisição POST padrão.
 * Lida com respostas JSON ou 'blob' (para arquivos).
 */
export async function post(route, data, expectedResponse = 'json') {

    const response = await fetch(`${window.location.origin}${route}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        let errorData;
        let errorMessage = "Erro no servidor.";

        try {
            // Tenta ler o corpo do erro como JSON
            errorData = await response.json();
            errorMessage = errorData.msg || `Erro ${response.status}`;
        } catch (e) {
            // Se falhar (ex: erro 500 com HTML), usa o status http
            errorMessage = `Erro ${response.status}: ${response.statusText}`;
            errorData = { details: "A resposta do erro não era JSON." };
        }

        const error = new Error(errorMessage);
        error.status = response.status;
        error.details = errorData;
        throw error;
    }

    if (expectedResponse === 'blob') {
        return response.blob();
    }

    return response.json();
}



export async function getClientInfo(cpf) {
    return post("/system/get_client_info/", { cpf: cpf });
}

export async function addClient(payload) {
    return post("/system/add_client/", payload);
}

export async function getClientEntrances(searchBy, value) {
     return post("/system/get_client_entrances/", {
        search: searchBy,
        "search-bar": value
    });
}

export async function adminCreateNewUser(payload) {
    return post("/admin/new/", payload);
}

export async function adminGetUserInfo(id) {
    return post("/admin/get_info/", { id: id });
}

export async function adminRunReport(payload) {
    return post("/admin/run_reports/", payload, 'blob');
}

export async function adminDeleteUser(id) {
    return post("/admin/delete/", { id: id });
}

export async function adminUpdateUser(payload) {
    return post("/admin/edit/", payload);
}