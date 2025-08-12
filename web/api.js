import axios from "axios";

const http = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Accounts API
export const getMe = () => http.get("/accounts/me");
