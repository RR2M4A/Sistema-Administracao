"use strict"

export function format_cpf(event) {

    event.preventDefault();

    let input = event.target;
    let start = input.selectionStart;
    let old_value = input.value;

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

    if (value.length > 14) {
        value = value.slice(0, 14);
    }

    input.value = value;
    
    let diff = input.value.length - old_value.length;
    input.setSelectionRange(start + diff, start + diff);

}


export function format_phone_number(event) {

    event.preventDefault();

    let input = event.target;
    let start = input.selectionStart;
    let old_value = input.value;

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

    let diff = input.value.length - old_value.length;
    input.setSelectionRange(start + diff, start + diff);

}


export function format_birth_date(event) {
    
    event.preventDefault();

    let input = event.target;
    let start = input.selectionStart;
    let old_value = input.value;

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

    let diff = input.value.length - old_value.length;
    input.setSelectionRange(start + diff, start + diff);
}