import { createRouter, createWebHistory } from "vue-router";
import { useStore } from "@/store";

import IndexPage from "@/components/index-page.vue";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/setup",
      name: "setup",
      component: () => import("@/components/setup-page.vue"),
    },
    {
      path: "/sign-in",
      name: "sign-in",
      component: () => import("@/components/signin-page.vue"),
    },
    {
      path: "/",
      name: "index",
      component: IndexPage,
      meta: {
        requiresAuth: true,
      },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const store = useStore();

  if (!store.isSiteMetaLoaded && to.name !== "setup") {
    next({ name: "setup" });
    return;
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.isAuthenticated) {
      next({
        name: "sign-in",
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
