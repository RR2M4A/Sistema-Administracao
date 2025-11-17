"use strict"


const adminBt = document.querySelector('.admin-bt');

adminBt?.addEventListener("click", evt => {
    window.location.assign(`${window.location.origin}/admin/`)
})