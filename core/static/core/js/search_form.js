'use strict'

const searchForm = document.querySelector('.search-client-form');
const searchBar = searchForm.querySelector('.search-bar');
const reloadBt = searchForm.querySelector('.reload-bt');
const searchClientBt = searchForm.querySelector('.search-client-bt');
const csrfToken = searchForm.querySelector('input[name="csrfmiddlewaretoken"]').value;
const entrancesTable = document.querySelector('.entrances-table');
const errorParagraph = document.querySelector('.search-client-form-error-msg');
const tableBody = document.querySelector('.entrances-table tbody');
const activatePopupBt = document.querySelector('.activate-popup-bt');
const newClientPopup = document.querySelector('.new-client-popup');
const overlay = document.querySelector('.overlay');


document.addEventListener('DOMContentLoaded', (evt) => {
    searchBar.focus();
})


searchBar.addEventListener('input', (evt) => {

    let start = searchBar.selectionStart;
    let oldValue = searchBar.value;

    let value = searchBar.value.replace(/\D/g, "");

    if (value.length == 0) {
        window.location.reload();
    }

    if (value.length > 3) {
        value = value.slice(0, 3) + "." + value.slice(3);
    }

    if (value.length > 7) {
        value = value.slice(0, 7) + "." + value.slice(7);
    }

    if (value.length > 11) {
        value = value.slice(0, 11) + "-" + value.slice(11);
    }

    if (value.length > 14) {
        value = value.slice(0, 14);
    }

    searchBar.value = value;

    let diff = searchBar.value.length - oldValue.length;
    searchBar.setSelectionRange(start + diff, start + diff);

})


reloadBt.addEventListener("click", (evt) => {
    evt.preventDefault();
    searchBar.value = '';
    window.location.reload();
})


searchClientBt.addEventListener("click", async (evt) => {
    evt.preventDefault();

    const cpf = searchBar.value;

    const response = await fetch(`${window.location.origin}/system/search/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ cpf: cpf })
    });

    const data = await response.json();


    // Text is erased after 5 seconds
    errorParagraph.innerHTML = data.message;

    // Updating table
    if (data.type == 'success') {

        errorParagraph.style.color = 'green';
        let citizen = data.dict.citizen
        tableBody.innerHTML = '';

        data.dict.entrances.forEach(entrance => {
            const row = `
                <tr>
                    <td>${citizen.name}</td>
                    <td>${citizen.cpf}</td>
                    <td>${citizen.phone_number}</td>
                    <td>${citizen.birth_date}</td>
                    <td>${entrance.department}</td>
                    <td>${entrance.entrance_date}</td>
                    <td>${entrance.entrance_time}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

    } else {
        errorParagraph.style.color = 'red';
    }

    setTimeout(() => {
        errorParagraph.innerHTML = '';
    }, 5000);

});


activatePopupBt.addEventListener("click", (evt) => {
    evt.preventDefault();
    newClientPopup.style.display = 'block';
    overlay.style.display = 'block';
})