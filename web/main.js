import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import { useStore } from "./store.js";

const app = createApp(App);

app.use(createPinia());
app.use(router);

async function initApp() {
  try {
    const store = useStore();
    await store.setLoggedInUser();
  } catch (error) {
    console.error("Error initializing app:", error);
  } finally {
    app.mount("#app");
  }
}

initApp();
