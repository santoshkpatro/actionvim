import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/:public_id',
      name: 'project-detail',
      component: () => import('@/views/ProjectDetailView.vue'),
    },
    {
      path: '/user/sign_in',
      name: 'login',
      component: () => import('@/views/user/SignInView.vue'),
      meta: { isPublic: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.isPublic || token) next()

  next({
    path: '/user/sign_in',
    query: { redirect: to.fullPath },
  })
})

export default router
