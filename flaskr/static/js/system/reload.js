"use strict"


const reload_bt = document.querySelector('.reload-bt');


export function init_listeners() {
    reload_bt.addEventListener("click", (event) => {
        event.preventDefault();
        window.location.reload();
    })
}

init_listeners();