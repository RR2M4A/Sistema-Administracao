"use strict"

const addNameInput = document.querySelector('#add-name');
const addCPFInput = document.querySelector('#add-cpf');
const addPhoneNumberInput = document.querySelector('#add-phone-number');
const addBirthDateInput= document.querySelector('#add-birth-date');
const addDepartmentInput = document.querySelector('#add-department');
const closePopupBt = document.querySelector('.close-popup-bt');
const overlay = document.querySelector('.overlay');
const popup = document.querySelector('.new-client-popup');
const csrfToken = popup.querySelector('input[name="csrfmiddlewaretoken"]').value;
const popupSideMsg = document.querySelector('.popup-side-msg');
const confirmBt = document.querySelector('.confirm-bt');

function clearErrors() {
    addCPFInput.style.border = '';
    addNameInput.style.border = '';
    addPhoneNumberInput.style.border = '';
    addBirthDateInput.style.border = '';
    addDepartmentInput.style.border = '';
}


function resetFormState() {
    addCPFInput.value = '';
    addNameInput.value = '';
    addPhoneNumberInput.value = '';
    addBirthDateInput.value = '';
    addDepartmentInput.value = '';

    addNameInput.disabled = true;
    addPhoneNumberInput.disabled = true;
    addBirthDateInput.disabled = true;
    addDepartmentInput.disabled = true;

    popupSideMsg.style.display = 'none';
    clearErrors();
}

addCPFInput.addEventListener("input", async (evt) => {

    let input = evt.target;
    let start = input.selectionStart;
    let oldValue = input.value;

    let value = input.value.replace(/\D/g, "");

    if (value.length > 3) {
        value = value.slice(0, 3) + "." + value.slice(3);
    }

    if (value.length > 7) {
        value = value.slice(0, 7) + "." + value.slice(7);
    }

    if (value.length > 11) {
        value = value.slice(0, 11) + "-" + value.slice(11);
    }

    if (value.length >= 14) {
        value = value.slice(0, 14);

        const response = await fetch(`${window.location.origin}/system/client-detail/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ cpf: input.value })
        });

        const data = await response.json();

        // Invalid CPF
        if (data.type == 'warning') {
            popupSideMsg.innerHTML = data.message;
            popupSideMsg.style.display = 'block';
            popupSideMsg.style.color = 'red';

            addNameInput.disabled = true;
            addPhoneNumberInput.disabled = true;
            addBirthDateInput.disabled = true;
            addDepartmentInput.disabled = true;

        // Client not found
        } else if (data.type == 'info') {
            popupSideMsg.innerHTML = data.message;
            popupSideMsg.style.display = 'block';
            popupSideMsg.style.color = 'green';

            addNameInput.value = '';
            addPhoneNumberInput.value = '';
            addBirthDateInput.value = '';

            addNameInput.disabled = false;
            addBirthDateInput.disabled = false;
            addPhoneNumberInput.disabled = false;
            addDepartmentInput.disabled = false;

            addNameInput.focus();
            clearErrors();

        // Client found
        } else if (data.type == 'success') {
            addNameInput.value = data.dict.name;
            addPhoneNumberInput.value = data.dict.phone_number;
            addBirthDateInput.value = data.dict.birth_date;

            if (data.dict.can_edit) {
                addNameInput.disabled = false;
                addBirthDateInput.disabled = false;
            } else {
                addNameInput.disabled = true;
                addBirthDateInput.disabled = true;
            }

            addPhoneNumberInput.disabled = false;
            addDepartmentInput.disabled = false;

            addDepartmentInput.focus();
            clearErrors();
        }

        setTimeout(() => {
            popupSideMsg.style.display = 'none';
        }, 5000);

    } else {
        // If user has deleted digits, it blocks again
        popupSideMsg.style.display = 'none';

        addNameInput.value = '';
        addPhoneNumberInput.value = '';
        addBirthDateInput.value = '';

        addNameInput.disabled = true;
        addPhoneNumberInput.disabled = true;
        addBirthDateInput.disabled = true;
        addDepartmentInput.disabled = true;

        clearErrors();
    }

    input.value = value;

    let diff = input.value.length - oldValue.length;
    input.setSelectionRange(start + diff, start + diff);
})

addPhoneNumberInput.addEventListener("input", (evt) => {

    let input = evt.target;
    let start = input.selectionStart;
    let oldValue = input.value;

    let value = input.value.replace(/\D/g, "");

    if (value.length > 0) {
        value = "(" + value;
    }

    if (value.length > 3) {
        value = value.slice(0, 3) + ") " + value.slice(3);
    }

    if (value.length > 9) {
        value = value.slice(0, 9) + "-" + value.slice(9);
    }

    if (value.length > 14) {
        value = value.replace("-", "");
        value = value.slice(0, 10) + "-" + value.slice(10, 14);
    }

    if (value.length > 15) {
        value = value.slice(0, 15);
    }

    input.value = value;

    let diff = input.value.length - oldValue.length;
    input.setSelectionRange(start + diff, start + diff);
})

addBirthDateInput.addEventListener("input", (evt) => {

    let input = evt.target;
    let start = input.selectionStart;
    let oldValue = input.value;

    let value = input.value.replace(/\D/g, "");

    if (value.length > 2) {
        value = value.slice(0, 2) + "/" + value.slice(2);
    }

    if (value.length > 5) {
        value = value.slice(0, 5) + "/" + value.slice(5);
    }

    if (value.length > 10) {
        value = value.slice(0, 10);
    }

    input.value = value;

    let diff = input.value.length - oldValue.length;
    input.setSelectionRange(start + diff, start + diff);
})

closePopupBt.addEventListener("click", (evt) => {
    evt.preventDefault();
    overlay.style.display = 'none';
    popup.style.display = 'none';
    resetFormState();
})

overlay.addEventListener("click", (evt) => {
    overlay.style.display = 'none';
    popup.style.display = 'none';
    resetFormState();
})

confirmBt.addEventListener("click", async (evt) => {
    evt.preventDefault();

    clearErrors();

    // Inputs data
    const payload = {
        name: addNameInput.value,
        cpf: addCPFInput.value,
        phone_number: addPhoneNumberInput.value,
        birth_date: addBirthDateInput.value,
        department: addDepartmentInput.value
    };

    // Element-name map
    const map = new Map([
        ['cpf', addCPFInput],
        ['phone_number', addPhoneNumberInput],
        ['name', addNameInput],
        ['birth_date', addBirthDateInput],
        ['department', addDepartmentInput],

    ])

    const response = await fetch(`${window.location.origin}/system/add/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (data.type == 'success') {
        window.location.reload();

    } else {
        for (const [element, error] of Object.entries(data.dict)) {
            map.get(element).style.border = '1px solid red';
        }
    }
})