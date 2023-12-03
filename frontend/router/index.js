import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import ProjectDetail from '@/views/ProjectDetail.vue'
import SignIn from '@/views/user/SignIn.vue'
import Edit from '@/views/Edit.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/:public_id',
      name: 'project-detail',
      component: ProjectDetail,
    },
    {
      path: '/user/sign_in',
      name: 'login',
      component: SignIn,
      meta: { isPublic: true },
    },
    {
      path: '/edit',
      name: 'edit',
      component: Edit,
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
