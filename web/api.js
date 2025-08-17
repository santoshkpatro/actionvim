import { notification } from "ant-design-vue";
import axios from "axios";
import Cookies from "js-cookie";

const http = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken") || "",
  },
});

http.interceptors.response.use(
  (response) => {
    const { success, message, data, details } = response.data;
    if (success && (message || details)) {
      notification.open({
        message: message,
        class: "success-notification",
        closeIcon: false,
        placement: "bottomRight",
        duration: 3,
        description: details || null,
      });
    }

    return data;
  },
  (error) => {
    const serverData = error.response?.data || {};
    const msg = serverData.message || "Something went wrong. Please try again.";
    const details = serverData.details || null;

    notification.open({
      message: msg,
      class: "error-notification",
      closeIcon: false,
      placement: "bottomRight",
      duration: 3,
      description: details,
    });

    return Promise.reject(error);
  }
);

export const getSiteMeta = () => http.get("/site-meta");
export const updateSiteMeta = (data) => http.patch("/site-meta", data);

// Accounts API
export const getMe = () => http.get("/accounts/me");
export const signInAPI = (data) => http.post("/accounts/sign-in", data);

// Application API
export const applicationsListAPI = () => http.get("/applications");
export const applicationsMineAPI = () => http.get("/applications/mine");

// Events API
export const eventsListAPI = (applicationId) =>
  http.get(`/applications/${applicationId}/events`);
export const eventsSchemaAPI = (applicationId) =>
  http.get(`/applications/${applicationId}/events/schema`);
