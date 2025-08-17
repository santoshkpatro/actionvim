import { createRouter, createWebHistory } from "vue-router";
import { useStore } from "@/store";

import ApplicationPage from "@/components/application-page.vue";

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
      path: "/application/create",
      name: "application-create",
      component: () => import("@/components/application-create.vue"),
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/application/:applicationId",
      component: ApplicationPage,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          name: "dashboard",
          path: "",
          component: () =>
            import("@/components/application/dashboard-page.vue"),
        },
        {
          name: "views",
          path: "views",
          component: () => import("@/components/application/views-page.vue"),
        },
      ],
    },
    {
      path: "/",
      component: () => import("@/components/index-page.vue"),
      name: "index",
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/components/not-found-page.vue"),
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
