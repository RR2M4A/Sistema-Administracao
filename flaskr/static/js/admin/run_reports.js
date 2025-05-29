'use strict';

import { fetchInfo } from "../utils/fetch_utils.js";
import { format_birth_date } from "../utils/formatters.js";

const overlay = document.querySelector('.overlay');
const reportBt = document.querySelector('.run-report-bt');
const generateReportsBt = document.querySelector('.generate-report-bt');
const reportBox = document.querySelector('.report-box');
const reportForm = document.querySelector('.report-box form');
const start_date = document.querySelector('.start-date');
const final_date = document.querySelector('.final-date');
const sideMsg = document.querySelector('.report-box__side-msg');


function loadReportBox() {
    overlay.style.display = "block";
    reportBox.style.display = "block";
}


function unloadReportBox() {
    overlay.style.display = "none";
    reportBox.style.display = "none";
    reportForm.reset();
}


async function runReports() {

    let entry = {
        "start-date": start_date.value,
        "final-date": final_date.value
    }

    let url = `${window.location.origin}/admin/run_reports/`;
    let response = await fetchInfo(url, entry);

    if (response.status != 200) {
        let data = await response.json();
        sideMsg.innerHTML = data['msg'];

    } else {

        let blob = await response.blob();

        url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "relatorio.xlsx";
        document.body.appendChild(a);

        a.click();
        a.remove();

        window.URL.revokeObjectURL(url);
        sideMsg.innerHTML = "";
        window.location.reload();
    }

}


function init_listeners() {
    generateReportsBt.addEventListener("click", evt => {
        evt.preventDefault();
        runReports();
    })

    reportBt.addEventListener("click", evt => {
        loadReportBox();
    })

    overlay.addEventListener("click", evt => {
        unloadReportBox();
    })

    start_date.addEventListener("input", evt => {
        format_birth_date(evt.target);
    })

    final_date.addEventListener("input", evt => {
        format_birth_date(evt.target);
    })
}


init_listeners();