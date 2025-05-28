"use strict"


export function make_entry(inputs) {

    const entry = {}

    for (let input of inputs) {
        if (input.type !== "radio" || input.checked) {
            entry[input.name] = input.value;
        }
    }

    return entry;

}

export async function fetchInfo(url = null, entry = {}) {

    url = url || window.location.href

    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(entry),
        headers: { "content-type": "application/json" }
    });

    return response;
}


export async function make_request(inputs, url=window.location.href) {

    let entry = make_entry(inputs);

    let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(entry),
        headers: {"content-type": "application/json"}
    });

    return response;

}

