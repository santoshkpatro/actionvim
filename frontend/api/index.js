import axios from "axios"

export const rawHttp = axios.create({
    baseURL: "/",
    withCredentials: false,
    responseType: "json"
})

export const http = axios.create({
    baseURL: "/",
    withCredentials: false,
    responseType: "json"
})
