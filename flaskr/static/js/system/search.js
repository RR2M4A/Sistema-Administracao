"use strict"

import { make_request } from "../utils/fetch_utils.js";


export async function search_client(event, inputs, search_msg) {

    event.preventDefault();
    res = await make_request(inputs);
}