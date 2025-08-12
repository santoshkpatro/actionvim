import { createRouter, createWebHistory } from "vue-router";

import IndexPage from "@/components/index-page.vue";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("../components/login-page.vue"),
    },
    {
      path: "/",
      name: "index",
      component: IndexPage,
    },
  ],
});

export default router;
