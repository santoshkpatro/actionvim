import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import { useStore } from "./store.js";
import "@/assets/main.css";

const app = createApp(App);

app.use(createPinia());

async function initApp() {
  try {
    const store = useStore();

    await store.loadSiteMeta();
    await store.setLoggedInUser();
  } catch (error) {
  } finally {
    app.use(router);
    app.mount("#app");
  }
}

initApp();
