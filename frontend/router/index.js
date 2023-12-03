import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresSignIn: true }
    },
    {
      path: '/:public_id',
      name: 'project-detail',
      component: () => import('@/views/ProjectDetailView.vue'),
      meta: { requiresSignIn: true }
    },
    {
      path: '/user/sign_in',
      name: 'login',
      component: () => import('@/views/user/SignInView.vue')
    }
  ]
})

router.beforeEach((to, from) => {
  // instead of having to check every route record with
  // to.matched.some(record => record.meta.requiresAuth)
  const user = localStorage.getItem("user")

  if (to.meta.requiresSignIn && !user) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: '/user/sign_in',
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    }
  }
})

export default router
